import os
from unittest import mock
import pytest
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env.test'))
from app.service.resumo_service import ResumoService
from app.dataprovider.database.model.resumo_entity import Resumo
from app.exception.excecao import (
    ExcecaoSalvarBancoDeDados,
    ExcecaoNaoEncontrado,
    ExcecaoValidacaoURL
)
from app.schema.resumo_schema import ResumoSaida


class MockResumoRepository:
    def buscar_por_url(self, url: str):
        return None

    def salvar(self, resumo: Resumo):
        return resumo

class MockWikipediaService:
    def verificar_url_wikipedia(self, url: str) -> bool:
        return True

    def obter_conteudo_wikipedia(self, url: str, max_caracteres: int) -> str:
        return "Conteudo teste"

@pytest.fixture
def resumo_service():
    resumo_repository = MockResumoRepository()
    wikipedia_service = MockWikipediaService()
    return ResumoService(resumo_repository=resumo_repository, wikipedia_service=wikipedia_service)

def test_gerar_resumo(resumo_service):
    conteudo = "Texto teste"
    palavras = 10

    with mock.patch('app.service.resumo_service.LLMChain.run', return_value='Resumo'):
        resumo = resumo_service.gerar_resumo(conteudo, palavras)
        assert isinstance(resumo, str)
        assert len(resumo.split()) <= palavras


def test_processar_resumo(resumo_service):
    url = "http://wikipedia.com/teste"
    palavras = 10

    with mock.patch('app.service.resumo_service.LLMChain.run', return_value='Resumo'):
        resumo_saida = resumo_service.processar_resumo(url, palavras)
        assert isinstance(resumo_saida, ResumoSaida)
        assert resumo_saida.url == url
        assert resumo_saida.palavras == palavras


def test_processar_resumo_url_invalida(resumo_service):
    with mock.patch.object(MockWikipediaService, 'verificar_url_wikipedia', return_value=False):
        with pytest.raises(ExcecaoValidacaoURL):
            resumo_service.processar_resumo("http://wikipedia.com/teste", 10)


def test_obter_resumo_existente(resumo_service):
    url = "http://wikipedia.com/teste"

    mock_resumo = Resumo(url=url, resumo="Resumo existente", palavras=10)
    with mock.patch.object(MockResumoRepository, 'buscar_por_url', return_value=mock_resumo):
        resumo_saida = resumo_service.obter_resumo_existente(url)
        assert resumo_saida.url == url
        assert resumo_saida.resumo == "Resumo existente"


def test_obter_resumo_existente_nao_encontrado(resumo_service):
    url = "http://wikipedia.com/teste"

    with mock.patch.object(MockResumoRepository, 'buscar_por_url', return_value=None):
        with pytest.raises(ExcecaoNaoEncontrado):
            resumo_service.obter_resumo_existente(url)

def test_processar_resumo_erro_salvamento(resumo_service):
    url = "http://wikipedia.com/teste"
    palavras = 10

    with mock.patch('app.service.resumo_service.LLMChain.run', return_value='Resumo'):
        with mock.patch.object(MockResumoRepository, 'salvar', side_effect=ExcecaoSalvarBancoDeDados("Erro ao salvar")):
            with pytest.raises(ExcecaoSalvarBancoDeDados):
                resumo_service.processar_resumo(url, palavras)
