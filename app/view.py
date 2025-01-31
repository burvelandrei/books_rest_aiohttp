from aiohttp import web
from pydantic import BaseModel, ValidationError
from typing import Optional


class BookSchema(BaseModel):
    name: str
    description: Optional[str]
    author_name: str


async def get_books(request):
    tasks = await request.app["db"].get_books()
    return web.json_response(data=tasks)

async def create_books(request):
    try:
        data = await request.json()
        BookSchema(**data)
    except ValidationError as e:
        raise web.HTTPBadRequest(text=str(e))

    await request.app["db"].create_book(
        name=data["name"],
        description=data.get("description"),
        author_name=data["author_name"],
    )

    return web.json_response({"message": "Book created"})

async def get_book(request):
    try:
        book_id = int(request.match_info["book_id"])
    except ValueError:
        return web.json_response({"error": "Invalid book ID"}, status=400)

    book = await request.app["db"].get_book(book_id)
    if book:
        return web.json_response(data=book)
    return web.json_response({"error": "Book not found"}, status=404)

async def delete_book(request):
    try:
        book_id = int(request.match_info["book_id"])
    except ValueError:
        return web.json_response({"error": "Invalid book ID"}, status=400)

    deleted = await request.app["db"].delete_book(book_id)
    if deleted:
        return web.json_response(status=204)
    return web.json_response({"error": "Book not found"}, status=404)