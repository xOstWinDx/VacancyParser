import abc

from src.domain.entity import Vacancy


class AbstractVacancyValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, vacancy: Vacancy) -> bool:
        raise NotImplementedError