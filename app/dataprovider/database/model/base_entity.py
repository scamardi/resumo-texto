from sqlalchemy.ext.declarative import declarative_base
from app.dataprovider.database.config.resumo_db_config import engine

BaseEntity = declarative_base()

def init():
    BaseEntity.metadata.create_all(bind=engine)