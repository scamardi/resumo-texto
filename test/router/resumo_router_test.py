import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env.test'))
import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from app.service.resumo_service import ResumoService
from app.schema.resumo_schema import ResumoEntrada, ResumoSaida
from app.exception.excecao import ExcecaoNaoEncontrado

app = FastAPI()

class MockResumoService:
    def processar_resumo(self, url: str, palavras: int):
        return ResumoSaida(url=url, resumo="Resumo teste", palavras=palavras)

    def obter_resumo_existente(self, url: str):
        return ResumoSaida(url=url, resumo="Resumo teste existente", palavras=10)

@app.post("/resumos", response_model=ResumoSaida)
async def criar_resumo(resumo_entrada: ResumoEntrada, resumo_service: ResumoService = Depends()):
    return resumo_service.processar_resumo(resumo_entrada.url, resumo_entrada.palavras)

@app.get("/resumos", response_model=ResumoSaida)
async def obter_resumo(url: str, resumo_service: ResumoService = Depends()):
    return resumo_service.obter_resumo_existente(url)

@pytest.fixture
def client():
    app.dependency_overrides[ResumoService] = lambda: MockResumoService()
    with TestClient(app) as c:
        yield c
    del app.dependency_overrides[ResumoService]

def test_criar_resumo(client):
    url = "http://wikipedia.com/teste"
    palavras = 10
    resumo_entrada = {"url": url, "palavras": palavras}
    response = client.post("/resumos", json=resumo_entrada)

    assert response.status_code == 200
    assert response.json() == {
        "url": url,
        "resumo": "Resumo teste",
        "palavras": palavras
    }

def test_obter_resumo(client):
    url = "http://wikipedia.com/teste"
    response = client.get(f"/resumos?url={url}")

    assert response.status_code == 200
    assert response.json() == {
        "url": url,
        "resumo": "Resumo teste existente",
        "palavras": 10
    }

def test_obter_resumo_nao_encontrado(client):
    class MockResumoServiceNotFound:
        def obter_resumo_existente(self, url: str):
            raise ExcecaoNaoEncontrado()

    app.dependency_overrides[ResumoService] = lambda: MockResumoServiceNotFound()
    url = "http://nonexistent.com"
    response = client.get(f"/resumos?url={url}")

    assert response.status_code == 404