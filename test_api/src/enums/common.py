from enum import Enum


class BaseEnum(Enum):


    @classmethod
    def as_value(cls):
        return [item.value for item in cls]


class HttpErrorCodes(int, BaseEnum):
    Ok: int = 200
    BadRequest: int = 400
    NotFound: int = 404
    MethodNotAllowed: int = 405

    def __int__(self) -> int:
        return int.__int__(self)