from typing import Dict, List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, RootModel

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
    ignored_attributes: Optional[List[str]] = None


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


class PredictedElement(BaseModel):
    element_id: str
    x: int
    y: int
    width: int
    height: int
    predicted_label: str
    predicted_probability: int
    sort_key: int


class PredictionResponseModel(RootModel):
    root: List[PredictedElement]


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


class PredictionRequest(BaseModel):
    document: str = Field(
        default="",
        description=(
            "Full HTML document for analysis. "
            "Every element should have jdn-hash attribute, which value must be unique "
            "across the document and should be unique across documents."
        ),
        example=(
            "<html lang=\"en\" jdn-hash=\"111111\">"
            "<body jdn-hash=\"222222\">"
            "<h1 jdn-hash=\"333333\">Hello</h1>"
            "</body></html>"
        ),
    )
    elements: str = Field(
        default="[]",
        description="JSON dumped to string, containing list of elements on page with some info about them.",
        example=(
            "["
                "{"
                    "\"tag_name\":\"BODY\","
                    "\"element_id\":\"222222\","
                    "\"parent_id\":\"111111\","
                    "\"x\":0,"
                    "\"y\":0,"
                    "\"width\":1070,"
                    "\"height\":969,"
                    "\"displayed\":true,"
                    "\"onmouseover\":null,"
                    "\"onmouseenter\":null,"
                    "\"attributes\":"
                    "{\"jdn-hash\":\"222222\"}"
                "}"
            "]"
        ),
    )
    viewport: Dict
