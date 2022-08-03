############################################
# this is a FastAPI-based backend
############################################

import os
from io import BytesIO

import aiohttp
import psutil
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi import status as status
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl

import app.mongodb as mongodb
from app import (
    MODEL_VERSION_DIRECTORY,
    UPLOAD_DIRECTORY,
    html5_df_path,
    mui_df_path,
    old_df_path,
    robula_api,
)
from app.models import PredictionInputModel, PredictionResponseModel, SystemInfoModel
from ds_methods.html5_predict import html5_predict_elements
from ds_methods.mui_predict import mui_predict_elements
from ds_methods.old_predict import predict_elements

os.makedirs(mui_df_path, exist_ok=True)
os.makedirs(old_df_path, exist_ok=True)
os.makedirs(html5_df_path, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

api = FastAPI()
api.include_router(robula_api.router)
templates = Jinja2Templates(directory="templates")


@api.get("/build")
async def build_version():
    """Build version."""
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
    """HTML elements prediction based on received JSON. Old model."""
    body = await request.body()
    return JSONResponse(await predict_elements(body))


@api.post("/mui-predict", response_model=PredictionResponseModel)
async def mui_predict(request: Request, input: PredictionInputModel):
    """HTML elements prediction based on received JSON. MUI model."""
    body = await request.body()
    return JSONResponse(await mui_predict_elements(body))


@api.post("/html5-predict", response_model=PredictionResponseModel)
async def html5_predict(request: Request, input: PredictionInputModel):
    """HTML elements prediction based on received JSON. HTML5 model."""
    body = await request.body()
    return JSONResponse(await html5_predict_elements(body))


@api.post("/bootstrap-predict", response_model=PredictionResponseModel)
async def bootstrap_predict(request: Request, input: PredictionInputModel):
    """Bootstrap elements prediction based on received JSON (HTML5 model)."""
    # The html5 model is currently sufficient for predicting the bootstrap
    # elements. Bootstrap model will be potentially developed and added later
    body = await request.body()
    return JSONResponse(await html5_predict_elements(body))


@api.get("/cpu-count")
async def cpu_count():
    return {"cpu_count": os.cpu_count()}


@api.get("/system_info", response_model=SystemInfoModel)
async def system_info():
    """Returns cpu count and total available memory in bytes"""
    total_memory = psutil.virtual_memory().total
    cpu_count = os.cpu_count()
    response = {"cpu_count": cpu_count, "total_memory": total_memory}

    return response


@api.get("/download_template")
async def download_template(
    repo_zip_url: HttpUrl = "https://github.com/jdi-templates/"
    "jdi-light-testng-empty-template/archive/refs/heads/main.zip",
):
    """Takes link to zip archive of repo from Github. Returns downloaded repo as zip"""
    headers = {"Content-Disposition": 'attachment; filename="template.zip"'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(repo_zip_url) as resp:
                if resp.status == 200:
                    content = await resp.read()

                    return StreamingResponse(content=BytesIO(content), headers=headers)

        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Connection Error: {e}")


@api.get("/show_request_info")
def show_request_data(request: Request):
    return {
        "client_host": request.client.host,
        "X-Real-Ip": request.headers.get("X-Real-Ip", None),
        "X-Forwarded-For": request.headers.get("X-Forwarded-For", None),
        "request_headers": request.headers,
    }


@api.get("/get_session_id")
def get_session_id():
    return mongodb.get_session_id()


@api.get("/export_logs")
def export_logs():
    mongodb.create_logs_json_file()
    return FileResponse("logs.json", filename="logs.json")


if __name__ == "__main__":
    uvicorn.run("app.main:api", host="127.0.0.1", port=5000, log_level="info")
