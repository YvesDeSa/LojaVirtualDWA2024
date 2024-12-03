from pydantic import BaseModel, field_validator

from util.validators import *

class InserirCategoriaDto(BaseModel):
    nome: str 

    @field_validator("nome")
    def validar_nome(cls, v):
        msg = is_size_between(v, "Nome", 2, 128)
        if msg: raise ValueError(msg)
        return v
