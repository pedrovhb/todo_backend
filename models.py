from typing import Union

from pydantic import BaseModel, Schema


class TodoBase(BaseModel):
    id_: str
    text: str = ...


class TodoBoolean(TodoBase):
    completed: bool = ...


class TodoCount(TodoBase):
    target_count: int = Schema(..., gt=0)
    current_count: int = Schema(0, ge=0)


class TodoTimer(TodoBase):
    target_time: int = Schema(..., gt=0)
    current_time: int = Schema(0, ge=0)


# Forms don't include ID
class TodoBooleanIn(BaseModel):
    text: str = Schema(..., min_length=1, max_length=200)
    completed: bool = False


class TodoCountIn(BaseModel):
    text: str = Schema(..., min_length=1, max_length=200)
    target_count: int = Schema(..., gt=0)
    current_count: int = Schema(0, ge=0)


class TodoTimerIn(BaseModel):
    text: str = Schema(..., min_length=1, max_length=200)
    target_time: int = Schema(..., gt=0)
    current_time: int = Schema(0, ge=0)


TodoModel: type = Union[TodoBoolean, TodoCount, TodoTimer]
TodoInModel: type = Union[TodoBooleanIn, TodoCountIn, TodoTimerIn]
# https://github.com/tiangolo/fastapi/issues/86#issuecomment-478536275