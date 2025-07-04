import logging

from src.application.usecase import StartParsersUseCase
from src.infrastructure.notifier import TelegramNotifier
from src.infrastructure.parser import TelegramVacancyParser
from src.infrastructure.validator import YandexVacancyValidator

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    use_case = StartParsersUseCase(
        class_parsers=(TelegramVacancyParser,),
        vacancy_validator=YandexVacancyValidator(),
        notifier=TelegramNotifier(),
    )
    use_case()
