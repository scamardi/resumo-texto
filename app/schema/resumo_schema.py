from pydantic import BaseModel

class ResumoEntrada(BaseModel):
    url: str
    palavras: int

class ResumoSaida(BaseModel):
    url: str
    resumo: str
    palavras: int

    class Config:
        orm_mode = True