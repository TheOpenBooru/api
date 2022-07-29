from starlette.middleware.base import BaseHTTPMiddleware
import logging

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # ip = request.scope['client'][0]
        # path = request.scope['path'] 
        # status = response.status_code
        # logging.info(f"{ip}:{path} - {status}")
        return response
