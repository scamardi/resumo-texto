import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

url_banco_de_dados = f"{os.getenv('POSTGRES_DIALECT')}://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOSTNAME')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(
    url_banco_de_dados, echo=False, future=True
)

sessao_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

def obter_conexao_banco():
    db = scoped_session(sessao_local)
    try:
        yield db
    finally:
        db.close()