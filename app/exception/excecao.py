from fastapi import HTTPException

class ExcecaoSalvarBancoDeDados(HTTPException):
    def __init__(self, detail: str = "Erro ao salvar o resumo no banco de dados.", erro: str = None):
        super().__init__(status_code=500, detail=detail)

class ExcecaoNaoEncontrado(HTTPException):
    def __init__(self, detail: str = "Resumo não encontrado.", erro: str = None):
        super().__init__(status_code=404, detail=detail)

class ExcecaoGeracaoResumo(HTTPException):
    def __init__(self, detail: str = "Erro na geração do resumo.", erro: str = None):
        super().__init__(status_code=500, detail=detail)

class ExcecaoAcessoURL(HTTPException):
    def __init__(self, detail: str = "Erro ao acessar a URL informada.", erro: str = None):
        super().__init__(status_code=500, detail=detail)

class ExcecaoTimeout(HTTPException):
    def __init__(self, detail: str = "A requisição está demorando muito tempo.", erro: str = None):
        super().__init__(status_code=500, detail=detail)

class ExcecaoValidacaoURL(HTTPException):
    def __init__(self, detail: str = "URL inválida. A URL deve ser da Wikipedia.", erro: str = None):
        super().__init__(status_code=400, detail=detail)

class ExcecaoGenerica(HTTPException):
    def __init__(self, detail: str = "Erro genérico.", erro: str = None):
        super().__init__(status_code=500, detail=detail)
