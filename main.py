
############################################
# this is a Flask-based backend
############################################

import os, gc
from flask import Flask, request, abort, jsonify, send_from_directory, json
import datetime as dt
import traceback

import pandas as pd
from utils import JDIDataset, JDIModel
import torch
import torch.nn as nn
from tqdm.auto import trange
from torch.utils.data import Dataset, DataLoader
import logging

UPLOAD_DIRECTORY = "flask-temp-storage"
JS_DIRECTORY = "js"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

api = Flask(__name__)
api.logger.setLevel(logging.DEBUG)

@api.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

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
    return jsonify({'status': 'OK'})

@api.route("/predict", methods=["POST"])
def predict():
    """Upload a file."""

    # generate temporary filename
    filename = dt.datetime.now().strftime("%Y%m%d%H%M%S%f.json")
    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        api.logger.info(f'saving {filename}')
        fp.write(request.data)
        fp.flush()
    
    filename = filename.replace('.json', '.parquet')
    api.logger.info(f'saving {filename}')
    df = pd.DataFrame(json.loads(request.data))

    # fix bad data which can come in 'onmouseover', 'onmouseenter'
    df.onmouseover = df.onmouseover.apply(lambda x: 'true' if x is not None else None)
    df.onmouseenter = df.onmouseenter.apply(lambda x: 'true' if x is not None else None)
    df.to_parquet(f'dataset/df/{filename}')

    api.logger.info('Creating JDIDataset')
    dataset = JDIDataset(dataset_names=[filename.split('.')[0]], rebalance=False)
    dataloader=DataLoader(dataset, shuffle=False, batch_size=1, collate_fn=dataset.collate_fn)

    device='cpu'

    api.logger.info(f'Load model with hardcoded device: {device}')
    model = torch.load('model/model.pth', map_location='cpu').to(device=device)
    model.eval()

    api.logger.info('Predicting...')
    results = []
    with trange(len(dataloader)) as bar:
        with torch.no_grad():
            for x, y in dataloader:
                x.to(device)
                y.to(device)
                y_pred = torch.round(torch.nn.Softmax(dim=1)(model(x.to(device)).to('cpu'))).detach().numpy()
                y_pred = y_pred[0].argmax()
                y = y.item()           
                
                results.append({
                    'y_true': y,
                    'y_pred': y_pred,
                    'y_true_label': dataset.classes_reverse_dict[y], 
                    'y_pred_label': dataset.classes_reverse_dict[y_pred]
                })
                bar.update(1)

    results_df = pd.DataFrame(results)
    dataset.dataset['predicted_label'] = results_df.y_pred_label

    results_df = dataset.dataset[dataset.dataset['predicted_label'] != 'n/a'][[
                                        'element_id', 
                                        'x', 
                                        'y', 
                                        'width', 
                                        'height', 
                                        'predicted_label'
                                    ]].copy()
                                    
    if results_df.shape[0] == 0:
        gc.collect()
        return jsonify([])
    else:
        del model
        gc.collect()
        return results_df.to_json(orient='records')

    # Return 201 CREATED
    #return jsonify({'status': 'OK', 'filename': filename})

# Start Flask server
if __name__ == "__main__":
    api.run(debug=False, port=5000, host='0.0.0.0')
