import asyncio

from pyrogram import Client

from src.config import settings

client = Client(
    name="my_account",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH
)

async def main():
    await client.start()  # Здесь введете номер и пароль
    await client.stop()  # Сессия сохранится в файл

asyncio.run(main())