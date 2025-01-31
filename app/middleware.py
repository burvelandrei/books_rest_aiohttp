import logging
import json
from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@web.middleware
async def request_logger_middleware(request, handler):
    """Логирует входящий запрос и исходящий ответ."""
    logger.info(f"Request: {request.method} {request.path}")

    try:
        response = await handler(request)
    except Exception as e:
        logger.exception(f"Error processing request: {e}")
        return web.json_response({"error": "Internal Server Error"}, status=500)

    logger.info(f"Response: {response.status}")
    return response