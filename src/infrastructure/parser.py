import asyncio
import logging
from multiprocessing import Queue

from pyrogram import Client, filters, raw
from pyrogram.types import Message

from src.config import settings
from src.domain.entity import Vacancy
from src.interfaces.parser import AbstractVacancyParser


class TelegramVacancyParser(AbstractVacancyParser):
    def __init__(self, queue: Queue):
        super().__init__(queue)

    async def _parse(self) -> None:
        app = Client(
            name="vacancy-parser",
            api_hash=settings.API_HASH,
            api_id=settings.API_ID
        )

        @app.on_message(filters.all)
        async def log_message(client: Client, message: Message):
            logging.info(
                f"Received message: {message.chat.title}: {message.chat.id} - {message.text[:20]}... | "
                f"allowed: {message.chat.id in settings.TELEGRAM_CHANNELS_IDS}"
            )

        @app.on_message(filters.chat(settings.TELEGRAM_CHANNELS_IDS))
        async def handle_message(client: Client, message: Message):
            vacancy = Vacancy(
                source=message.chat.title,
                title=message.text[:message.text.find("\n") + 1],
                text=message.text,
                publish_date=message.date
            )
            self.queue.put(vacancy)

        # Запуск клиента
        async with app:
            while True:
                await asyncio.sleep(1)
