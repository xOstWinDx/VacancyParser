import abc

from src.domain.entity import Vacancy


class AbstractNotifier(abc.ABC):
    @abc.abstractmethod
    async def notify(self, vacancy: Vacancy):
        raise NotImplementedError