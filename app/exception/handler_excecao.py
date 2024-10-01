from fastapi import FastAPI, Request
import logging
import uuid
import traceback

from app.exception.excecao import ExcecaoGenerica

app = FastAPI()
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def handler_excecao_generica(request: Request, e: Exception):
    correlation_id = request.headers.get("correlationId", str(uuid.uuid4()))
    error_traceback = traceback.format_exc()

    logger.error({
        "correlation_id": correlation_id,
        "error": {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": error_traceback,
        },
        "request": {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
        }
    })

    raise ExcecaoGenerica(str(e))
