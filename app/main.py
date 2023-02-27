############################################
# this is a FastAPI-based backend
############################################
import base64
import os
import smtplib
from io import BytesIO
from typing import Dict, Union

import aiohttp
import psutil
import uvicorn
from fastapi import FastAPI, HTTPException, Request, UploadFile
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
from app.logger import logger
from app.models import (
    PredictionInputModel,
    PredictionResponseModel,
    ReportMail,
    SystemInfoModel,
)
from app.tasks import send_report_mail_task
from ds_methods.angular_predict import angular_predict_elements
from ds_methods.html5_predict import html5_predict_elements
from ds_methods.mui_predict import mui_predict_elements
from utils.config import SMTP_HOST
from utils.api_utils import sort_predict_body


os.makedirs(mui_df_path, exist_ok=True)
os.makedirs(old_df_path, exist_ok=True)
os.makedirs(html5_df_path, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

api = FastAPI()
api.include_router(robula_api.router)
templates = Jinja2Templates(directory="templates")


@api.get("/build")
def build_version() -> str:
    """Build version."""
    files = []
    for filename in os.listdir(MODEL_VERSION_DIRECTORY):
        path = os.path.join(MODEL_VERSION_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files[-1]


api.version = build_version()


@api.get("/files")
async def dir_listing(request: Request) -> templates.TemplateResponse:
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
async def get_file(path: str) -> FileResponse:
    """Download a file."""
    return FileResponse(
        filename=path,
        path=os.path.join(UPLOAD_DIRECTORY, path),
        media_type="application/json",
    )


@api.post("/mui-predict", response_model=PredictionResponseModel)
async def mui_predict(request: Request, input: PredictionInputModel) -> JSONResponse:
    """HTML elements prediction based on received JSON. MUI model."""
    body = await request.body()
    body_sorted = sort_predict_body(request_body=body)

    return JSONResponse(await mui_predict_elements(body_sorted))


@api.post("/angular-predict", response_model=PredictionResponseModel)
async def angular_predict(
    request: Request, input: PredictionInputModel
) -> JSONResponse:
    """HTML elements prediction based on received JSON. Angular model."""
    body = await request.body()
    body_sorted = sort_predict_body(request_body=body)

    return JSONResponse(await angular_predict_elements(body_sorted))


@api.post("/html5-predict", response_model=PredictionResponseModel)
async def html5_predict(request: Request, input: PredictionInputModel) -> JSONResponse:
    """HTML elements prediction based on received JSON. HTML5 model."""
    body = await request.body()
    body_sorted = sort_predict_body(request_body=body)

    return JSONResponse(await html5_predict_elements(body_sorted))


@api.get("/cpu-count")
async def cpu_count() -> Dict:
    return {"cpu_count": os.cpu_count()}


@api.get("/system_info", response_model=SystemInfoModel)
async def system_info() -> Dict:
    """Returns cpu count and total available memory in bytes"""
    total_memory = psutil.virtual_memory().total
    cpu_count = os.cpu_count()
    response = {"cpu_count": cpu_count, "total_memory": total_memory}

    return response


@api.get("/download_template")
async def download_template(
    repo_zip_url: HttpUrl = "https://github.com/jdi-templates/"
    "jdi-light-testng-empty-template/archive/refs/heads/main.zip",
) -> StreamingResponse:
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


@api.get("/get_session_id")
def get_session_id() -> int:
    return mongodb.get_session_id()


@api.get("/export_logs")
def export_logs() -> FileResponse:
    mongodb.create_logs_json_file()
    return FileResponse("logs.json", filename="logs.json")


@api.get("/ping_smtp")
def ping_smtp() -> Union[str, int]:
    try:
        s = smtplib.SMTP(SMTP_HOST, 587, timeout=10)
        s.starttls()
    except Exception as e:
        logger.info(f"Got Exception during pinging smtp.yandex.ru: '{e}'")
        return f"Got Exception during pinging smtp.yandex.ru: '{e}'"
    else:
        return 1


@api.post("/report_problem")
async def report_problem(msg_content: ReportMail):
    send_report_mail_task.apply_async(kwargs={"msg_content": msg_content.dict()})


@api.post("/file_bytes_to_str")
async def file_bytes_to_str(file: UploadFile):
    file_in_bytes = await file.read()
    file_in_str = base64.b64encode(file_in_bytes).decode()
    return file_in_str


if __name__ == "__main__":
    uvicorn.run("app.main:api", host="127.0.0.1", port=5000, log_level="info")
