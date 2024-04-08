from typing import Dict, List, Optional, Union

from pydantic import BaseModel, EmailStr, Field

from app.constants import CeleryStatuses


class TaskIdModel(BaseModel):
    id: Union[str, List[str]]


class TaskStatusModel(TaskIdModel):
    status: CeleryStatuses


class TaskResultModel(TaskIdModel):
    result: str


class RobulaSettingsModel(BaseModel):
    maximum_generation_time: Optional[int] = None
    allow_indexes_at_the_beginning: bool = False
    allow_indexes_in_the_middle: bool = True
    allow_indexes_at_the_end: bool = True
    advanced_calculation: bool = False


class XPathGenerationModel(TaskIdModel):
    document: str
    config: RobulaSettingsModel


class CSSSelectorGenerationModel(TaskIdModel):
    document: str


class LoggingInfoModel(BaseModel):
    session_id: int
    element_library: str
    page_object_creation: str
    website_url: str
    locator_list: List = []


class PredictionRequestElement(BaseModel):
    tag_name: Union[str, None]
    element_id: Union[str, None]
    parent_id: Union[str, None]
    x: Union[int, None]
    y: Union[int, None]
    width: Union[int, None]
    height: Union[int, None]
    displayed: Union[bool, None]
    onmouseover: Union[str, None]
    onmouseenter: Union[str, None]
    attributes: Union[Dict, None]
    text: Union[str, None]


class PredictionInputModel(BaseModel):
    document: str
    elements: str


class PredictedElement(BaseModel):
    element_id: str
    x: int
    y: int
    width: int
    height: int
    predicted_label: str
    predicted_probability: int
    sort_key: int


class PredictionResponseModel(BaseModel):
    __root__: List[PredictedElement]


class Attachment(BaseModel):
    filename: str
    file_content: str


class ReportMail(BaseModel):
    email: EmailStr = Field(..., alias="from")
    subject: Optional[str] = Field(..., max_length=200)
    body: str = Field(..., max_length=10000)
    attachments: Optional[List[Attachment]]


class SystemInfoModel(BaseModel):
    cpu_count: int
    total_memory: int
