import enum
from typing import List
from typing import Optional

from pydantic import BaseModel


class CeleryStatuses(str, enum.Enum):
    PENDING = 'PENDING'
    RECEIVED = 'RECEIVED'
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    REVOKED = 'REVOKED'
    REJECTED = 'REJECTED'
    RETRY = 'RETRY'
    IGNORED = 'IGNORED'


class TaskIdModel(BaseModel):
    id: str


class TaskIdsModel(BaseModel):
    id: List[str]


class TaskStatusModel(BaseModel):
    id: str
    status: CeleryStatuses


class TaskResultModel(BaseModel):
    id: str
    result: str


class RobulaSettingsModel(BaseModel):
    maximum_generation_time: Optional[int] = None
    allow_indexes_at_the_beginning: bool = False
    allow_indexes_in_the_middle: bool = True
    allow_indexes_at_the_end: bool = True


class XPathGenerationModel(TaskIdModel):
    document: str
    config: RobulaSettingsModel
