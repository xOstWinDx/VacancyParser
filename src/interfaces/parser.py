import abc
import asyncio
import inspect
from multiprocessing import Queue

from src.domain.entity import Vacancy


class AbstractVacancyParser(abc.ABC):

    def __init__(self, queue: Queue):
        self.queue = queue

    @abc.abstractmethod
    def _parse(self) -> None:
        raise NotImplementedError

    def run(self):
        """Автоматически определяет, как запускать parse()."""

        # Проверяем, является ли parse корутиной
        is_coroutine = inspect.iscoroutinefunction(self._parse)

        if is_coroutine:
            # Если асинхронный — запускаем через asyncio
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            new_loop.create_task(self._parse())
            new_loop.run_forever()
        else:
            # Если синхронный — вызываем напрямую
            return self._parse()
