import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue, Process

from src.domain.entity import Vacancy
from src.interfaces.notifier import AbstractNotifier
from src.interfaces.parser import AbstractVacancyParser
from src.interfaces.validator import AbstractVacancyValidator


class StartParsersUseCase:
    def __init__(
        self,
        class_parsers: tuple[type[AbstractVacancyParser]],
        vacancy_validator: AbstractVacancyValidator,
        notifier: AbstractNotifier,
        vacancy_queue: Queue = Queue()

    ) -> None:
        self.class_parsers = class_parsers
        self.vacancy_validator = vacancy_validator
        self.vacancy_queue = vacancy_queue
        self.notifier = notifier

    def __call__(self):
        for parser in self.class_parsers:
            Process(
                target=self.worker,
                args=(parser, self.vacancy_queue),
                daemon=True
            ).start()
        while True:
            vacancy = self.vacancy_queue.get() # Бесконечно ждём новых сообщений
            logging.debug(f"Received message: {vacancy}")
            if not self.vacancy_validator.validate(vacancy):
                logging.info(f"Vacancy {vacancy} is invalid")
                continue

            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.notifier.notify(vacancy))
            except Exception:
                logging.exception("Failed to send message")


    @staticmethod
    def worker(
        parser_class: type[AbstractVacancyParser],
        queue: Queue,
    ):
        parser = parser_class(queue)
        parser.run()  # блокируем выполнение
