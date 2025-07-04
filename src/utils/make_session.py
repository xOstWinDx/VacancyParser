import asyncio
from datetime import datetime

from pyrogram import Client

from src.config import settings

client = Client(
    name="vacancy-parser",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH
)

async def main():
    await client.start()
    chat = await client.get_chat("myresume_ru")
    print(chat)

    async for message in client.get_chat_history("myresume_ru", limit=1):
        print(message)
    await client.stop()  # Сессия сохранится в файл

asyncio.run(main())