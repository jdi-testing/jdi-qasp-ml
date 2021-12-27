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
from app import robula_api
from ds_methods.mui_predict import mui_predict_elements
from ds_methods.old_predict import predict_elements

os.makedirs(mui_df_path, exist_ok=True)
os.makedirs(old_df_path, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

api = FastAPI()
api.include_router(robula_api.router)
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


@api.get('/files')
async def dir_listing(request: Request):
    # Joining the base and the requested path

    if not os.path.exists(UPLOAD_DIRECTORY):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File not found")

    if os.path.isfile(UPLOAD_DIRECTORY):
        return FileResponse(UPLOAD_DIRECTORY)

    files = os.listdir(UPLOAD_DIRECTORY)

    return templates.TemplateResponse("files.html", {"request": request, "files": files})


@api.get("/files/{path:path}")
async def get_file(path: str):
    """Download a file."""
    return FileResponse(filename=path, path=os.path.join(UPLOAD_DIRECTORY, path), media_type="application/json")


@api.post("/predict")
async def predict(request: Request):
    """ HTML elements prediction based on received JSON. Old model. """
    body = await request.body()
    return JSONResponse(await predict_elements(body))


@api.post("/mui-predict")
async def mui_predict(request: Request):
    """ HTML elements prediction based on received JSON. MUI model. """
    body = await request.body()
    return JSONResponse(await mui_predict_elements(body))


if __name__ == '__main__':
    uvicorn.run("app.main:api", host="127.0.0.1", port=5000, log_level="info")
