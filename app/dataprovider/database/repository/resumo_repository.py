from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dataprovider.database.config.resumo_db_config import obter_conexao_banco
from app.dataprovider.database.model.resumo_entity import Resumo

class ResumoRepository:
    db: Session

    def __init__(self, db: Session = Depends(obter_conexao_banco)) -> None:
        self.db = db

    def salvar(self, resumo: Resumo) -> Resumo:
        self.db.add(resumo)
        self.db.commit()
        self.db.refresh(resumo)
        return resumo

    def buscar_por_url(self, url: str) -> Optional[Resumo]:
        return self.db.query(Resumo).filter(Resumo.url == url).first()