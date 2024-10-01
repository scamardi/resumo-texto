from fastapi import FastAPI
from app.exception.handler_excecao import handler_excecao_generica
from app.logging.logging_config import setup_logging
from app.router import resumo_router
from app.logging.logging_interceptor import log_request
from prometheus_fastapi_instrumentator import Instrumentator

setup_logging()

app = FastAPI()

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

app.middleware('http')(log_request)
app.add_exception_handler(Exception, handler_excecao_generica)
app.include_router(resumo_router.router)