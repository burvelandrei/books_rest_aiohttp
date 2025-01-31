import asyncpg
import asyncio
from typing import List, Dict, Optional

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn, min_size=1, max_size=10)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def create_book(
        self,
        name: str,
        description: str,
        author_name: str,
    ) -> int:

        query = """
        INSERT INTO books (name, description, author_name)
        VALUES ($1, $2, $3)
        """
        async with self.pool.acquire() as conn:
            await conn.fetchval(query, name, description, author_name)

    async def get_books(self) -> List[Dict]:
        query = """
        SELECT id, name, description, author_name
        FROM books
        """
        async with self.pool.acquire() as conn:
            books = await conn.fetch(query)
            return [dict(book) for book in books]

    async def get_book(self, book_id: int) -> Optional[Dict]:

        query = """
        SELECT id, name, description, author_name
        FROM books
        WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            book = await conn.fetchrow(query, book_id)
            return dict(book) if book else None


    async def delete_book(self, book_id: int) -> bool:
        query = """
        DELETE FROM books
        WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, book_id)
            return result == "DELETE 1"