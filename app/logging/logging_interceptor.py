import logging
import os
import uuid
from fastapi import Request

logger = logging.getLogger(__name__)

async def log_request(request: Request, call_next):
    correlation_id = request.headers.get("correlationId", str(uuid.uuid4()))
    request_data = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": await request.json() if request.method in ["POST", "PUT", "PATCH"] else None,
    }

    response = await call_next(request)

    response_data = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
    }

    log_data = {
        "app_name": os.getenv("APP_NAME"),
        "correlation_id": correlation_id,
        "request": request_data,
        "response": response_data,
    }
    logger.info("", extra=log_data)

    return response
