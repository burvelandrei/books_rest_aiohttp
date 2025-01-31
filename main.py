from aiohttp import web

from app.urls import setup_routes
from app.database import Database
from config import DATABASE, SERVER
from app.middleware import request_logger_middleware


async def init_app():
    app = web.Application(middlewares=[request_logger_middleware])

    db = Database(
        dsn="postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **DATABASE
        )
    )
    await db.connect()
    app["db"] = db

    setup_routes(app)

    async def close_db(app):
        yield
        await db.disconnect()

    app.cleanup_ctx.append(close_db)

    return app

if __name__ == "__main__":
    web.run_app(init_app(), host=SERVER["host"], port=int(SERVER["port"]))
