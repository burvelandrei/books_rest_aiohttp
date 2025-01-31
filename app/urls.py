from .view import get_books, create_books, get_book, delete_book


def setup_routes(app):
    app.router.add_get("/books/", get_books)
    app.router.add_post("/books/", create_books)

    app.router.add_get("/books/{book_id:\\d+}/", get_book)
    app.router.add_delete("/books/{book_id:\\d+}/", delete_book)
