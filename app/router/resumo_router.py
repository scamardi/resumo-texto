from fastapi import APIRouter, Depends
from app.service.resumo_service import ResumoService
from app.schema.resumo_schema import ResumoEntrada, ResumoSaida

router = APIRouter()

@router.post("/resumos", response_model=ResumoSaida)
async def criar_resumo(resumo_entrada: ResumoEntrada, resumo_service: ResumoService = Depends()):
    return resumo_service.processar_resumo(resumo_entrada.url, resumo_entrada.palavras)

@router.get("/resumos", response_model=ResumoSaida)
async def obter_resumo(url: str, resumo_service: ResumoService = Depends()):
    return resumo_service.obter_resumo_existente(url)
