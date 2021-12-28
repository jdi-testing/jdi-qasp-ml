import enum


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


class WebSocketResponseActions(str, enum.Enum):
    STATUS_CHANGED = "status_changed"
    RESULT_READY = "result_ready"
    TASKS_SCHEDULED = "tasks_scheduled"
