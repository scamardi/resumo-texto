import requests
from unittest.mock import patch, MagicMock
from app.service.wikipedia_service import WikipediaService
from app.exception.excecao import ExcecaoAcessoURL, ExcecaoTimeout

def test_verificar_url_wikipedia_valida():
    url_valida = "https://pb.wikipedia.org/teste"
    assert WikipediaService.verificar_url_wikipedia(url_valida) is True

def test_verificar_url_wikipedia_invalida():
    url_invalida = "https://teste.wikipedia.com"
    assert WikipediaService.verificar_url_wikipedia(url_invalida) is False

@patch('app.service.wikipedia_service.requests.get')
def test_obter_conteudo_wikipedia_sucesso(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'<p>Conteudo Wikipedia</p>'
    mock_get.return_value = mock_response
    url = "https://wikipedia.org/"
    conteudo = WikipediaService.obter_conteudo_wikipedia(url, max_caracteres=100)

    assert conteudo == "Conteudo Wikipedia"

@patch('app.service.wikipedia_service.requests.get')
def test_obter_conteudo_wikipedia_erro_http(mock_get):
    mock_get.side_effect = requests.HTTPError("Erro 404")
    url = "https://wikipedia.org/"
    try:
        WikipediaService.obter_conteudo_wikipedia(url, max_caracteres=100)
    except ExcecaoAcessoURL:
        assert True
    else:
        assert False

@patch('app.service.wikipedia_service.requests.get')
def test_obter_conteudo_wikipedia_timeout(mock_get):
    mock_get.side_effect = requests.Timeout
    url = "https://wikipedia.org/"
    try:
        WikipediaService.obter_conteudo_wikipedia(url, max_caracteres=100)
    except ExcecaoTimeout:
        assert True
    else:
        assert False
