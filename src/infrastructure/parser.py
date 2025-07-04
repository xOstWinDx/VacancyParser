import asyncio
import logging
from multiprocessing import Queue

from pyrogram import Client, filters
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
        async def handle_message(client: Client, message: Message):
            if message.text is None or message.chat is None:
                logging.info(f"Received message with no text or chat: {message}")
                return
            if message.chat.id not in settings.TELEGRAM_CHANNELS_IDS:
                logging.info(f"Received message from disallowed channel: {message}")
                return

            logging.info(
                f"Received message: {message.chat.title}: {message.chat.id} - {message.text[:20]}..."
            )

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
