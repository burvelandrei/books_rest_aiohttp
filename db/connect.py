import asyncpg
from asyncpg.exceptions import PostgresError
from environs import Env


env = Env()
env.read_env()


connection = None

async def connect():
    global connection
    connection = await asyncpg.connect(
        user=env("DB_USER"),
        password=env("DB_PASSWORD"),
        database=env("DB_NAME"),
        host=env("DB_HOST"),
        port=int(env("DB_PORT"))
    )

async def close():
    global connection
    if connection is not None:
        await connection.close()
        connection = None

async def fetch(query, *args):
    if connection is None:
        raise RuntimeError("Database connection is not established. Call connect() first.")

    try:
        return await connection.fetch(query, *args)
    except PostgresError as e:
        print(f"Database error in fetch: {e}")
        raise

async def execute(query, *args):
    if connection is None:
        raise RuntimeError("Database connection is not established. Call connect() first.")

    try:
        return await connection.execute(query, *args)
    except PostgresError as e:
        print(f"Database error in execute: {e}")
        raise