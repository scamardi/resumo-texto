import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../../../.env.test'))
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dataprovider.database.model.resumo_entity import Resumo
from app.dataprovider.database.repository.resumo_repository import ResumoRepository

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()
    Resumo.metadata.create_all(bind=engine)
    yield session
    session.close()

@pytest.fixture
def resumo_repository(test_db):
    return ResumoRepository(db=test_db)

def test_salvar_resumo(resumo_repository):
    resumo = Resumo(url="http://teste.com", resumo="Resumo teste", palavras=2)
    saved_resumo = resumo_repository.salvar(resumo)

    assert saved_resumo.url == "http://teste.com"
    assert saved_resumo.resumo == "Resumo teste"
    assert saved_resumo.palavras == 2

def test_buscar_por_url(resumo_repository):
    resumo = Resumo(url="http://teste.com", resumo="Resumo teste", palavras=2)
    resumo_repository.salvar(resumo)
    found_resumo = resumo_repository.buscar_por_url("http://teste.com")

    assert found_resumo is not None
    assert found_resumo.url == "http://teste.com"
    assert found_resumo.resumo == "Resumo teste"

def test_buscar_por_url_nao_encontrado(resumo_repository):
    found_resumo = resumo_repository.buscar_por_url("http://teste.com")

    assert found_resumo is None
