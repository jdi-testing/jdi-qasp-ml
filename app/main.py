############################################
# this is a Flask-based backend
############################################

import datetime as dt
import gc
import logging
import os
import pickle

import pandas as pd
import torch
from flask import (
    Flask,
    request,
    abort,
    jsonify,
    send_from_directory,
    json,
    render_template,
    send_file,
)
from torch.utils.data import DataLoader
from tqdm.auto import trange

from app import (
    UPLOAD_DIRECTORY,
    TEMPLATES_PATH,
    MODEL_VERSION_DIRECTORY,
    JS_DIRECTORY,
    mui_df_path,
    mui_model,
    old_df_path,
    old_model,
    html5_df_path,
    html5_model,
    html5_classes_path,
)
from utils.dataset import MUI_JDNDataset, HTML5_JDNDataset
from app.robula_api import robula_api

from utils_old.dataset import JDNDataset as Old_JDNDataset

os.makedirs(mui_df_path, exist_ok=True)
os.makedirs(old_df_path, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

api = Flask("app.main", template_folder=TEMPLATES_PATH)
api.logger.setLevel(logging.DEBUG)
api.register_blueprint(robula_api)


@api.route("/build")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(MODEL_VERSION_DIRECTORY):
        path = os.path.join(MODEL_VERSION_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/files", defaults={"req_path": ""})
def dir_listing(req_path):
    # Joining the base and the requested path
    abs_path = os.path.join(UPLOAD_DIRECTORY, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template("files.html", files=files)


@api.route("/js")
def list_js():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(JS_DIRECTORY):
        path = os.path.join(JS_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route("/js/<path:path>")
def get_js_script(path):
    """Download a file."""
    return send_from_directory(JS_DIRECTORY, path, as_attachment=False)


@api.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return jsonify({"status": "OK"})


@api.route("/predict", methods=["POST"])
def predict():
    """Upload a file."""

    # create softmax layser function to get probabilities from logits
    softmax = torch.nn.Softmax(dim=1)

    # generate temporary filename
    filename = dt.datetime.now().strftime("%Y%m%d%H%M%S%f.json")
    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        api.logger.info(f"saving {filename}")
        fp.write(request.data)
        fp.flush()

    filename = filename.replace(".json", ".pkl")
    api.logger.info(f"saving {filename}")
    df = pd.DataFrame(json.loads(request.data))

    # fix bad data which can come in 'onmouseover', 'onmouseenter'
    df.onmouseover = df.onmouseover.apply(lambda x: "true" if x is not None else None)
    df.onmouseenter = df.onmouseenter.apply(lambda x: "true" if x is not None else None)
    with open(f"{old_df_path}/{filename}.pkl", "wb") as f:
        pickle.dump(df, f)
        f.flush()

    df.to_pickle(f"{old_df_path}/{filename}")

    api.logger.info("Creating JDNDataset")
    dataset = Old_JDNDataset(
        datasets_list=[filename.split(".")[0]], rebalance_and_shuffle=False
    )
    dataloader = DataLoader(dataset, shuffle=False, batch_size=1)

    device = "cpu"

    api.logger.info(f"Load model with hardcoded device: {device}")
    model = torch.load(f"{old_model}/model.pth", map_location="cpu").to(device=device)
    model.eval()

    api.logger.info("Predicting...")
    results = []
    with trange(len(dataloader)) as bar:
        with torch.no_grad():
            for x, y in dataloader:
                x.to(device)
                y.to(device)
                y_prob = softmax(model(x.to(device)).to("cpu")).detach().numpy()

                y_pred = y_prob[0].argmax()
                y = y.item()
                y_prob = y_prob[0, y_pred].item()

                results.append(
                    {
                        "y_true": y,
                        "y_pred": y_pred,
                        "y_probability": y_prob,
                        "y_true_label": dataset.classes_reverse_dict[y],
                        "y_pred_label": dataset.classes_reverse_dict[y_pred],
                    }
                )
                bar.update(1)

    results_df = pd.DataFrame(results)

    # update the dataset with predictions
    dataset.df["predicted_label"] = results_df.y_pred_label.values
    dataset.df["predicted_probability"] = results_df.y_probability.values

    columns_to_publish = [
        "element_id",
        "x",
        "y",
        "width",
        "height",
        "predicted_label",
        "predicted_probability",
    ]

    results_df = dataset.df[
        (dataset.df["predicted_label"] != "n/a")  # & (dataset.df['is_hidden'] == 0)
    ][columns_to_publish].copy()
    # sort in descending order: big controls first
    results_df["sort_key"] = results_df.height * results_df.width
    results_df = results_df.sort_values(by="sort_key", ascending=False)

    if results_df.shape[0] == 0:
        gc.collect()
        return jsonify([])
    else:
        del model
        gc.collect()
        return results_df.to_json(orient="records")

    # Return 201 CREATED
    # return jsonify({'status': 'OK', 'filename': filename})


@api.route("/mui-predict", methods=["POST"])
def mui_predict():
    """Upload a file."""

    # create softmax layser function to get probabilities from logits
    softmax = torch.nn.Softmax(dim=1)

    # generate temporary filename
    filename = dt.datetime.now().strftime("%Y%m%d%H%M%S%f.json")
    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        api.logger.info(f"saving {filename}")
        fp.write(request.data)
        fp.flush()

    filename = filename.replace(".json", ".pkl")
    api.logger.info(f"saving {filename}")
    df = pd.DataFrame(json.loads(request.data))

    # fix bad data which can come in 'onmouseover', 'onmouseenter'
    df.onmouseover = df.onmouseover.apply(lambda x: "true" if x is not None else None)
    df.onmouseenter = df.onmouseenter.apply(lambda x: "true" if x is not None else None)

    df.to_pickle(f"{mui_df_path}/{filename}")

    api.logger.info("Creating JDNDataset")
    dataset = MUI_JDNDataset(
        datasets_list=[filename.split(".")[0]], rebalance_and_shuffle=False
    )
    dataloader = DataLoader(dataset, shuffle=False, batch_size=1)

    device = "cpu"

    api.logger.info(f"Load model with hardcoded device: {device}")
    model = torch.load(f"{mui_model}/model.pth", map_location="cpu").to(device=device)
    model.eval()

    api.logger.info("Predicting...")
    results = []
    with trange(len(dataloader)) as bar:
        with torch.no_grad():
            for x, y in dataloader:

                x.to(device)
                y.to(device)
                y_prob = softmax(model(x.to(device)).to("cpu")).detach().numpy()

                y_pred = y_prob[0].argmax()

                if y != torch.tensor([0]):
                    api.logger.info(f"y is\n {y} ")
                    api.logger.info(f"y_pred is\n {y_pred} ")

                y = y.item()
                y_prob = y_prob[0, y_pred].item()

                results.append(
                    {
                        "y_true": y,
                        "y_pred": y_pred,
                        "y_probability": y_prob,
                        "y_true_label": dataset.classes_reverse_dict[y],
                        "y_pred_label": dataset.classes_reverse_dict[y_pred],
                    }
                )
                bar.update(1)

    results_df = pd.DataFrame(results)

    # # update the dataset with predictions
    dataset.df["predicted_label"] = results_df.y_pred_label.values
    dataset.df["predicted_probability"] = results_df.y_probability.values

    columns_to_publish = [
        "element_id",
        "x",
        "y",
        "width",
        "height",
        "predicted_label",
        "predicted_probability",
    ]

    results_df = dataset.df[
        (dataset.df["predicted_label"] != "n/a") & (dataset.df["is_hidden"] == 0)
    ][columns_to_publish].copy()
    # # sort in descending order: big controls first
    results_df["sort_key"] = results_df.height * results_df.width
    results_df = results_df.sort_values(by="sort_key", ascending=False)

    if results_df.shape[0] == 0:
        gc.collect()
        return jsonify([])
    else:
        del model
        gc.collect()
        return results_df.to_json(orient="records")


@api.route("/html5-predict", methods=["POST"])
def html5_predict():

    # generate temporary filename
    filename = dt.datetime.now().strftime("%Y%m%d%H%M%S%f.json")
    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        api.logger.info(f"saving {filename}")
        fp.write(request.data)
        fp.flush()

    filename = filename.replace(".json", ".pkl")
    api.logger.info(f"saving {filename}")
    df = pd.DataFrame(json.loads(request.data))

    # fix bad data which can come in 'onmouseover', 'onmouseenter'
    df.onmouseover = df.onmouseover.apply(lambda x: "true" if x is not None else None)
    df.onmouseenter = df.onmouseenter.apply(lambda x: "true" if x is not None else None)

    df.to_pickle(f"{html5_df_path}/{filename}")

    api.logger.info("Creating JDNDataset")
    dataset = HTML5_JDNDataset(
        datasets_list=[filename.split(".")[0]],
        dataset_type="html5",
        rebalance_and_shuffle=False,
    )
    # load model
    api.logger.info("Loading the model")
    pkl_filename = "DT_model.pkl"
    with open(f"{html5_model}/{pkl_filename}", "rb") as file:
        model = pickle.load(file)

    # classes dictionaries
    with open(html5_classes_path, "r") as f:
        lines = f.readlines()
        encoder_dict = {line.strip(): i for i, line in enumerate(lines)}
        decoder_dict = {v: k for k, v in encoder_dict.items()}

    api.logger.info("Predicting...")
    dataset.df["predicted_label"] = (
        pd.Series(model.predict(dataset.X))
        .apply(lambda x: decoder_dict.get(x, "n/a"))
        .values
    )
    dataset.df["predicted_probability"] = model.predict_proba(dataset.X).max(axis=1)

    columns_to_publish = [
        "element_id",
        "is_hidden",
        "x",
        "y",
        "width",
        "height",
        "predicted_label",
        "predicted_probability",
    ]

    results_df = dataset.df[(dataset.df["predicted_label"] != "n/a")][
        columns_to_publish
    ].copy()
    # # sort in descending order: big controls first
    results_df["sort_key"] = results_df.height * results_df.width
    results_df = results_df.sort_values(by="sort_key", ascending=False)

    if results_df.shape[0] == 0:
        gc.collect()
        return jsonify([])
    else:
        del model
        gc.collect()
        return results_df.to_json(orient="records")
