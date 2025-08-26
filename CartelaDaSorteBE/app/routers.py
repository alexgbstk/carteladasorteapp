from fastapi import APIRouter, HTTPException
from . import services, schemas

router = APIRouter()


@router.post("/NovaCartela", response_model=schemas.Cartela)
async def nova_cartela():
    return await services.nova_cartela()


@router.post("/ApostarNaCartela", response_model=schemas.ApostaResp)
async def apostar(req: schemas.ApostaReq):
    try:
        return await services.apostar(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/AtualizarCartela", response_model=schemas.Cartela)
async def atualizar(numero_sorteio: str | None = None):
    try:
        return await services.atualizar(numero_sorteio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/SortearCartela", response_model=schemas.SortearResp)
async def sortear(req: schemas.AtualizarReq):
    try:
        return await services.sortear(req.numero_sorteio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
