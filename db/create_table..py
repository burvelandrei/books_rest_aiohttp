import asyncio
from connect import connect, close, execute

async def create_tables():
    # Подключаемся к базе данных
    await connect()

    try:
        # Создаем таблицу authors
        await execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)

        # Создаем таблицу categories
        await execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)

        # Создаем таблицу books
        await execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                author_id INT REFERENCES authors(id) ON DELETE CASCADE,
                category_id INT REFERENCES categories(id) ON DELETE CASCADE
            );
        """)

        print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        # Закрываем подключение
        await close()

if __name__ == "__main__":
    asyncio.run(create_tables())