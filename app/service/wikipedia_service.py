import re
import requests
from bs4 import BeautifulSoup
from app.exception.excecao import ExcecaoAcessoURL, ExcecaoTimeout


class WikipediaService:

    @staticmethod
    def verificar_url_wikipedia(url: str) -> bool:
        padrao = r'^https?:\/\/(www\.)?(wikipedia\.org|[a-z]{2}\.wikipedia\.org)(\/)?'
        return re.match(padrao, url) is not None

    def obter_conteudo_wikipedia(url: str, max_caracteres: int) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.HTTPError as e:
            raise ExcecaoAcessoURL(erro=str(e))
        except requests.Timeout:
            raise ExcecaoTimeout()

        soup = BeautifulSoup(response.content, "html.parser")
        conteudo = " ".join([p.text for p in soup.find_all("p")])
        return conteudo[:max_caracteres]