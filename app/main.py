############################################
# this is a Flask-based backend
############################################

import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi import status as status
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app import MODEL_VERSION_DIRECTORY
from app import UPLOAD_DIRECTORY
from app import mui_df_path
from app import old_df_path
from app import html5_df_path
from app import html5_model
from app import html5_classes_path
from app import robula_api
from app import websocket
from app.models import PredictionInputModel, PredictionResponseModel
from ds_methods.mui_predict import mui_predict_elements
from ds_methods.old_predict import predict_elements

os.makedirs(mui_df_path, exist_ok=True)
os.makedirs(old_df_path, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

api = FastAPI()
api.include_router(robula_api.router)
api.include_router(websocket.router)
templates = Jinja2Templates(directory="templates")

logger = logging.getLogger("jdi-qasp-ml")


@api.get("/build")
async def build_version():
    """ Build version. """
    files = []
    for filename in os.listdir(MODEL_VERSION_DIRECTORY):
        path = os.path.join(MODEL_VERSION_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return JSONResponse(files)


@api.get("/files")
async def dir_listing(request: Request):
    # Joining the base and the requested path

    if not os.path.exists(UPLOAD_DIRECTORY):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File not found")

    if os.path.isfile(UPLOAD_DIRECTORY):
        return FileResponse(UPLOAD_DIRECTORY)

    files = os.listdir(UPLOAD_DIRECTORY)

    return templates.TemplateResponse(
        "files.html", {"request": request, "files": files}
    )


@api.get("/files/{path:path}")
async def get_file(path: str):
    """Download a file."""
    return FileResponse(
        filename=path,
        path=os.path.join(UPLOAD_DIRECTORY, path),
        media_type="application/json",
    )


@api.post("/predict", response_model=PredictionResponseModel)
async def predict(request: Request, input: PredictionInputModel):
    """ HTML elements prediction based on received JSON. Old model. """
    body = await request.body()
    return JSONResponse(await predict_elements(body))


@api.post("/mui-predict", response_model=PredictionResponseModel)
async def mui_predict(request: Request, input: PredictionInputModel):
    """ HTML elements prediction based on received JSON. MUI model. """
    body = await request.body()
    return JSONResponse(await mui_predict_elements(body))


@api.get("/cpu-count")
async def cpu_count():
    return {"cpu_count": os.cpu_count()}


if __name__ == "__main__":
    uvicorn.run("app.main:api", host="127.0.0.1", port=5000, log_level="info")

# @api.route("/html5-predict", methods=["POST"])
# def html5_predict():

#     # generate temporary filename
#     filename = dt.datetime.now().strftime("%Y%m%d%H%M%S%f.json")
#     with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
#         api.logger.info(f"saving {filename}")
#         fp.write(request.data)
#         fp.flush()

#     filename = filename.replace(".json", ".pkl")
#     api.logger.info(f"saving {filename}")
#     df = pd.DataFrame(json.loads(request.data))

#     # fix bad data which can come in 'onmouseover', 'onmouseenter'
#     df.onmouseover = df.onmouseover.apply(lambda x: "true" if x is not None else None)
#     df.onmouseenter = df.onmouseenter.apply(lambda x: "true" if x is not None else None)

#     df.to_pickle(f"{html5_df_path}/{filename}")

#     api.logger.info("Creating JDNDataset")
#     dataset = HTML5_JDNDataset(
#         datasets_list=[filename.split(".")[0]],
#         dataset_type="html5",
#         rebalance_and_shuffle=False,
#     )
#     # load model
#     api.logger.info("Loading the model")
#     pkl_filename = "DT_model.pkl"
#     with open(f"{html5_model}/{pkl_filename}", "rb") as file:
#         model = pickle.load(file)

#     # classes dictionaries
#     with open(html5_classes_path, "r") as f:
#         lines = f.readlines()
#         encoder_dict = {line.strip(): i for i, line in enumerate(lines)}
#         decoder_dict = {v: k for k, v in encoder_dict.items()}

#     api.logger.info("Predicting...")
#     dataset.df["predicted_label"] = (
#         pd.Series(model.predict(dataset.X))
#         .apply(lambda x: decoder_dict.get(x, "n/a"))
#         .values
#     )
#     dataset.df["predicted_probability"] = model.predict_proba(dataset.X).max(axis=1)

#     columns_to_publish = [
#         "element_id",
#         "is_hidden",
#         "x",
#         "y",
#         "width",
#         "height",
#         "predicted_label",
#         "predicted_probability",
#     ]

#     results_df = dataset.df[(dataset.df["predicted_label"] != "n/a")][
#         columns_to_publish
#     ].copy()
#     # # sort in descending order: big controls first
#     results_df["sort_key"] = results_df.height * results_df.width
#     results_df = results_df.sort_values(by="sort_key", ascending=False)

#     if results_df.shape[0] == 0:
#         gc.collect()
#         return jsonify([])
#     else:
#         del model
#         gc.collect()
#         return results_df.to_json(orient="records")
