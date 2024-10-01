import os
from fastapi import Depends
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from app.dataprovider.database.repository.resumo_repository import ResumoRepository
from app.dataprovider.database.model.resumo_entity import Resumo
from app.exception.excecao import (
    ExcecaoSalvarBancoDeDados,
    ExcecaoNaoEncontrado,
    ExcecaoValidacaoURL,
    ExcecaoGeracaoResumo
)
from app.schema.resumo_schema import ResumoSaida
from app.service.wikipedia_service import WikipediaService

class ResumoService:
    def __init__(self,
                 resumo_repository: ResumoRepository = Depends(),
                 wikipedia_service: WikipediaService = Depends()):
        self.resumo_repository = resumo_repository
        self.wikipedia_service = wikipedia_service

    @staticmethod
    def gerar_resumo(conteudo: str, palavras: int) -> str:
        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
        template = "Resuma o seguinte texto em até {palavras} palavras:\n\n{conteudo}"
        prompt = ChatPromptTemplate.from_messages([HumanMessagePromptTemplate.from_template(template)])
        chain = LLMChain(llm=llm, prompt=prompt)

        try:
            return chain.run({"palavras": palavras, "conteudo": conteudo})
        except Exception as e:
            raise ExcecaoGeracaoResumo(erro=str(e))

    def processar_resumo(self, url: str, palavras: int, max_caracteres: int = 2000):
        if not self.wikipedia_service.verificar_url_wikipedia(url):
            raise ExcecaoValidacaoURL()

        resumo_existente = self.resumo_repository.buscar_por_url(url)
        if resumo_existente:
            return resumo_existente

        conteudo = self.wikipedia_service.obter_conteudo_wikipedia(url, max_caracteres)
        resumo = self.gerar_resumo(conteudo, palavras)

        novo_resumo = Resumo(url=url, resumo=resumo, palavras=palavras)
        try:
            self.resumo_repository.salvar(novo_resumo)
        except Exception as e:
            raise ExcecaoSalvarBancoDeDados(erro=str(e))

        return ResumoSaida(url=novo_resumo.url, resumo=novo_resumo.resumo, palavras=novo_resumo.palavras)

    def obter_resumo_existente(self, url: str):
        resumo = self.resumo_repository.buscar_por_url(url)
        if not resumo:
            raise ExcecaoNaoEncontrado()
        return ResumoSaida(url=resumo.url, resumo=resumo.resumo, palavras=resumo.palavras)
