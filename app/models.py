from typing import List, Union, Dict
from typing import Optional

from pydantic import BaseModel

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


class XPathGenerationModel(TaskIdModel):
    document: str
    config: RobulaSettingsModel


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
    __root__: List[PredictionRequestElement]


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
