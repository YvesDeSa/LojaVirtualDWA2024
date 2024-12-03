import asyncio
from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import JSONResponse

from dtos.alterar_pedido_dto import AlterarPedidoDto
from dtos.alterar_produto_dto import AlterarProdutoDto
from dtos.id_produto_dto import IdProdutoDto
from dtos.inserir_produto_dto import InserirProdutoDto
from dtos.problem_details_dto import ProblemDetailsDto
from models.categoria_model import Categoria
from models.pedido_model import EstadoPedido
from models.produto_model import Produto
from repositories.item_pedido_repo import ItemPedidoRepo
from repositories.pedido_repo import PedidoRepo
from repositories.produto_repo import ProdutoRepo
from repositories.usuario_repo import UsuarioRepo
from repositories.categoria_repo import CategoriaRepo



router = APIRouter(prefix="/admin")
SLEEP_TIME = 0.2


@router.get("/obter_produtos")
async def obter_produtos():
    await asyncio.sleep(1)
    produtos = ProdutoRepo.obter_todos()
    return produtos

@router.post("/inserir_produto", status_code=201)
async def inserir_produto(inputDto: InserirProdutoDto) -> Produto:
    novo_produto = Produto(None, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    novo_produto = ProdutoRepo.inserir(novo_produto)
    return novo_produto

@router.post("/excluir_produto", status_code=204)
async def excluir_produto(inputDto: IdProdutoDto):
    if ProdutoRepo.excluir(inputDto.id_produto): return None
    pd = ProblemDetailsDto("int", f"O produto com id <b>{inputDto.id_produto}</b> não foi encontrado.", "value_not_found", ["body", "id_produto"])
    return JSONResponse(pd.to_dict(), status_code=404)

@router.get("/obter_produto/{id_produto}")
async def obter_produto(id_produto: int = Path(..., title="Id do Produto", ge=1)):
    produto = ProdutoRepo.obter_um(id_produto)
    if produto: return produto
    pd = ProblemDetailsDto("int", f"O produto com id <b>{id_produto}</b> não foi encontrado.", "value_not_found", ["body", "id_produto"])
    return JSONResponse(pd.to_dict(), status_code=404)

@router.post("/alterar_produto", status_code=204)
async def alterar_produto(inputDto: AlterarProdutoDto):
    produto = Produto(inputDto.id, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    if ProdutoRepo.alterar(produto): return None
    pd = ProblemDetailsDto("int", f"O produto com id <b>{inputDto.id}</b> não foi encontrado.", "value_not_found", ["body", "id"])
    return JSONResponse(pd.to_dict(), status_code=404)

@router.post("/alterar_pedido", status_code=204)
async def alterar_pedido(inputDto: AlterarPedidoDto):
    if PedidoRepo.alterar_estado(inputDto.id, inputDto.estado.value): 
        return None
    pd = ProblemDetailsDto("int", f"O pedido com id <b>{inputDto.id}</b> não foi encontrado.", "value_not_found", ["body", "id"])
    return JSONResponse(pd.to_dict(), status_code=404)

@router.post("/cancelar_pedido/{id_pedido}", status_code=204)
async def cancelar_pedido(id_pedido: int = Path(..., title="Id do Pedido", ge=1)):
    if PedidoRepo.alterar_estado(id_pedido, EstadoPedido.CANCELADO.value): 
        return None
    pd = ProblemDetailsDto("int", f"O pedido com id <b>{id_pedido}</b> não foi encontrado.", "value_not_found", ["body", "id"])
    return JSONResponse(pd.to_dict(), status_code=404)

@router.post("/evoluir_pedido/{id_pedido}", status_code=204)
async def cancelar_pedido(id_pedido: int = Path(..., title="Id do Pedido", ge=1)):
    pedido = PedidoRepo.obter_por_id(id_pedido)
    if not pedido:
        pd = ProblemDetailsDto("int", f"O pedido com id <b>{id_pedido}</b> não foi encontrado.", "value_not_found", ["body", "id"])
        return JSONResponse(pd.to_dict(), status_code=404)
    estado_atual = pedido.estado
    estados = [e.value for e in list(EstadoPedido) if e != EstadoPedido.CANCELADO]
    indice = estados.index(estado_atual)
    indice += 1
    if indice < len(estados):
        novo_estado = estados[indice]
        if PedidoRepo.alterar_estado(id_pedido, novo_estado): 
            return None
    pd = ProblemDetailsDto("int", f"O pedido com id <b>{id_pedido}</b> não pode ter seu estado evoluído para <b>cancelado</b>.", "state_change_invalid", ["body", "id"])
    return JSONResponse(pd.to_dict(), status_code=404)
    

@router.get("/obter_pedido/{id_pedido}")
async def obter_pedido(id_pedido: int = Path(..., title="Id do Pedido", ge=1)):
    # TODO: refatorar criando Dto com resultado específico
    pedido = PedidoRepo.obter_por_id(id_pedido)
    if pedido:
        itens = ItemPedidoRepo.obter_por_pedido(pedido.id)
        cliente = UsuarioRepo.obter_por_id(pedido.id_cliente)
        pedido.itens = itens
        pedido.cliente = cliente
        return pedido
    pd = ProblemDetailsDto("int", f"O pedido com id <b>{id_pedido}</b> não foi encontrado.", "value_not_found", ["body", "id"])
    return JSONResponse(pd.to_dict(), status_code=404)

@router.get("/obter_pedidos_por_estado/{estado}")
async def obter_pedidos_por_estado(estado: EstadoPedido = Path(..., title="Estado do Pedido")):    
    await asyncio.sleep(1)
    pedidos = PedidoRepo.obter_todos_por_estado(estado.value)
    return pedidos


@router.get("/obter_produtos_por_categoria/{id_categoria}")
async def obter_produtos_por_categoria(
    id_categoria: int = Path(..., title="Id da Categoria", ge=1)
):
    await asyncio.sleep(SLEEP_TIME)
    produtos = ProdutoRepo.obter_por_categoria(id_categoria)
    return produtos

@router.get("/obter_categorias")
async def obter_categorias():
    await asyncio.sleep(SLEEP_TIME)
    categorias = CategoriaRepo.obter_todos()
    return categorias

@router.get("/obter_categorias/{id_categoria}")
async def obter_categoria(id_categoria: int = Path(..., title="Id da Categoria", ge=1)):
    await asyncio.sleep(SLEEP_TIME)
    categoria = CategoriaRepo.obter_um(id_categoria)
    if categoria:
        return categoria
    pd = ProblemDetailsDto(
        "int",
        f"A categoria com id <b>{id_categoria}</b> não foi encontrada.",
        "value_not_found",
        ["body", "id_categoria"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)



@router.post("/adicionar_categoria", response_model=Categoria, status_code=201)
async def adicionar_categoria(categoria: Categoria):
    """
    Adiciona uma nova categoria.
    """
    await asyncio.sleep(SLEEP_TIME)
    nova_categoria = CategoriaRepo.inserir(categoria)
    if not nova_categoria:
        raise HTTPException(status_code=500, detail="Erro ao adicionar categoria")
    return nova_categoria


@router.post("/editar_categoria", response_model=Categoria)
async def editar_categoria(categoria: Categoria):
    """
    Edita uma categoria existente.
    """
    await asyncio.sleep(SLEEP_TIME)
    sucesso = CategoriaRepo.alterar(categoria)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria



@router.post("/excluir_categoria/{id_categoria}", status_code=204)
async def excluir_categoria(
    id_categoria: int = Path(..., title="ID da Categoria", ge=1)
):
    await asyncio.sleep(SLEEP_TIME)
    sucesso = CategoriaRepo.excluir(id_categoria)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return