from pydantic import BaseModel, field_validator

from util.validators import *


class IdUserDto(BaseModel):
    id_user: int

    @field_validator("id_user")
    def validar_id_user(cls, v):
        msg = is_greater_than(v, "Id do User", 0)
        if msg: raise ValueError(msg)
        return v