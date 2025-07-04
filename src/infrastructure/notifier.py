import asyncio
import logging

import aiohttp

from src.config import settings
from src.domain.entity import Vacancy
from src.interfaces.notifier import AbstractNotifier


class TestNotifier(AbstractNotifier):
    async def notify(self, vacancy: Vacancy):
        logging.info(f"In test notifier received vacancy: {vacancy}")
        print(vacancy)


class TelegramNotifier(AbstractNotifier):
    async def notify(self, vacancy: Vacancy):
        logging.debug(f"In telegram notifier received vacancy: {vacancy}")

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

        for _ in range(20):
            try:
                async with (aiohttp.ClientSession() as session):
                    async with session.post(
                            url,
                            json={
                                "chat_id": settings.TELEGRAM_ADMIN_ID,
                                "text": vacancy.to_html(),
                                "parse_mode": "HTML"
                            }
                    ) as r:
                        if r.status == 200:
                            break
                        if r.status == 429:
                            logging.error("Too many requests, waiting 10 seconds")
                            await asyncio.sleep(10)
                            continue
                        logging.error("Failed to send message: %s, status code: %s", await r.text(), r.status)
                        return
            except Exception:
                logging.exception("Failed to send message")
                return
        else:
            logging.exception("Failed to send message after 20 attempts")
            return
