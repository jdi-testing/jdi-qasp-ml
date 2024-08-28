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
    element_id: str = Field(description="Value of `jdn-hash` element attribute")
    predicted_label: str = Field(description="Label predicted by model")
    childs: Optional[List[str]] = Field(description="List of `jdn-hash`es of child elements predicted by model")
    displayed: bool = Field(description="Visibility status of element predicted by model")
    is_shown: bool = Field(description="Visibility status of element determined in Selenium")


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


class ViewportInfo(BaseModel):
    width: int = Field(..., description="Viewport width in pixels")
    height: int = Field(..., description="Viewport height in pixels")


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
            "<body id=\"body\" jdn-hash=\"222222\">"
            "<h1 jdn-hash=\"333333\">Hello</h1>"
            "</body></html>"
        ),
    )
    elements: str = Field(
        default="[]",
        description=(
            "JSON dumped to string, containing list of elements on page with some info about them.\n\n"
            "Documentation for objects fields. Sometimes JS code is used to describe values. In this case `el` will "
            "be used to refer to page element.\n\n"
            "`tag_name`: Tag name of the element, uppercased. `el.tagName`\n\n"
            "`element_id`: Value of `jdn-hash` attribute for this element.\n\n"
            "`parent_id`: Value of `jdn-hash` attribute of parent element. Null if element doesn't have parent.\n\n"
            "`x`: Result of `window.pageXOffset + el.getBoundingClientRect().x`\n\n"
            "`y`: Result of `window.pageYOffset + el.getBoundingClientRect().y`\n\n"
            "`width`: `el.getBoundingClientRect().width`\n\n"
            "`height`: `el.getBoundingClientRect().height`\n\n"
            "`displayed`: Boolean value. True if `x > 0` or `y > 0` or `height >= 1` or `width >= 1`.\n\n"
            "`onmouseover`: `el.onmouseover`\n\n"
            "`onmouseenter`: `el.onmouseenter`\n\n"
            "`attributes`: Object containing all of element attributes and their values (see payload example).\n\n"
            "`text`: Rendered text content of the element and its descendants. `el.innerText`"
        ),
        example=(
            "["
                "{"  # noqa: E131
                    "\"tag_name\":\"BODY\","  # noqa: E131
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
                        "{\"id\": \"body\", \"jdn-hash\":\"222222\"},"  # noqa: E131
                    "\"text\": \"Hello\""
                "}"
            "]"
        ),
    )
    viewport: Optional[str] = Field(
        default=None,
        description=(
            "JSON dumped to string, containing object with viewport width and height in pixels.\n\n"
            "If null or omitted, browser default viewport size will be used.\n\n"
            "Documentation for object fields.\n\n"
            "`width`: Width of the viewport in pixels.\n\n"
            "`height`: Height of the viewport in pixels.\n\n"
        ),
        example=(
            "{"
                "\"width\": 1920,"  # noqa: E131
                "\"height\": 1080"
            "}"
        ),
    )
