import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger

class ProcessTimeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)

        return response
    
class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"completed_in={process_time:.4f}s "
            f"status_code={response.status_code}"
        )

        return response