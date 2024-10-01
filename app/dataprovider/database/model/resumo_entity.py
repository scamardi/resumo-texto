from sqlalchemy import Column, String, Integer
from app.dataprovider.database.model.base_entity import BaseEntity

class Resumo(BaseEntity):
    __tablename__ = "resumo"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String, unique=True, index=True)
    resumo = Column(String)
    palavras = Column(Integer)