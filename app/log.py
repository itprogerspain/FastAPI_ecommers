from uuid import uuid4
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger

logger.add(
    "info.log",
    rotation="10 MB",
    retention="20 days",
    format="Log: [{extra[log_id]}:{time} - {level} - {message}]",
    level="INFO",
    enqueue = True
)


async def log_middleware(request: Request, call_next):
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        try:
            response = await call_next(request)

            if 400 <= response.status_code < 500:
                logger.warning(f"Client error {response.status_code} at {request.url.path}")
            elif 500 <= response.status_code < 600:
                logger.error(f"Server error {response.status_code} at {request.url.path}")
            else:
                logger.info(f"Successfully accessed {request.url.path}")

        except Exception as ex:
            logger.exception(f"Unhandled exception at {request.url.path}")  # exception = traceback + message
            response = JSONResponse(
                content={"success": False, "detail": str(ex)},
                status_code=500,
            )

        return response