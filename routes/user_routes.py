import asyncio
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dtos.id_user_dto import IdUserDto
from dtos.problem_details_dto import ProblemDetailsDto
from repositories.usuario_repo import UsuarioRepo


router = APIRouter(prefix="/admin")


@router.get("/obter_users")
async def obter_produtos():
    print("Users")
    await asyncio.sleep(1)
    users = UsuarioRepo.obter_todos_por_perfil()
    return users

@router.post("/excluir_user", status_code=204)
async def excluir_user(inputDto: IdUserDto):
    if UsuarioRepo.excluir(inputDto.id_user): return None
    pd = ProblemDetailsDto("int", f"O Usuário com id <b>{inputDto.id_user}</b> não foi encontrado.", "value_not_found", ["body", "id_user"])
    return JSONResponse(pd.to_dict(), status_code=404)

