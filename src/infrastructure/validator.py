import logging
import re

from yandex_cloud_ml_sdk import YCloudML

from src.config import settings
from src.domain.entity import Vacancy
from src.interfaces.validator import AbstractVacancyValidator


class TestVacancyValidator(AbstractVacancyValidator):
    def validate(self, vacancy: Vacancy) -> bool:
        return True


class YandexVacancyValidator(AbstractVacancyValidator):
    PYTHON_VACANCY_PATTERN = re.compile(
        r"(?ix)"
        r"(?:"
        r"\b(?:python|питон|пайтон)\b.*?\b(?:backend|бекенд|разработчик|developer|программист|engineer)\b"
        r"|"
        r"\b(?:fastapi|django|flask|asyncio|aiohttp|sqlalchemy|pydantic|celery)\b"
        r"|"
        r"\b(?:postgresql|postgres|mysql|mongodb|kafka|redis|clickhouse)\b"
        r")"
        r"(?!.*\b(?:java\b|javascript\b|js\b|с\#|1с|1c|frontend|фронтенд|react|angular|vue)\b)"
    )

    def validate(self, vacancy: Vacancy) -> bool:
        if not self.PYTHON_VACANCY_PATTERN.search(vacancy.text):
            logging.info(f"Vacancy <{vacancy.text[:20]}>  - is not Python (not matched by pattern)")
            return False

        # Если регулярка прошла — проверяем через LLM
        messages = [
            {
                "role": "system",
                "text": """
                    Ты — анализатор вакансий. Чётко следуй правилам:
                    Вакансия подходит, если ВСЕ условия выполнены:
                    1. Должность: Python-бэкенд (если не указано — не подходит)
                    2. Технологии: Требуется FastAPI
                    3. Формат: Удалёнка или не указано
                    4. Уровень: Мидл/Джуниор/Не указан (если Senior — не подходит)
                    Ответ только "Yes" или "No"
                    Никаких других слов, точек или пояснений!
                """,
            },
            {
                "role": "user",
                "text": vacancy.text,
            }
        ]

        sdk = YCloudML(
            folder_id="b1gh5k33r0kkd785m3me",
            auth=settings.LLM_API_KEY,
        )

        result = sdk.models.completions("llama-lite", model_version="latest").configure(temperature=0.3).run(messages)
        res = result[0].text.strip().lower().rstrip(".")
        if res == "yes":
            return True
        logging.info(f"Vacancy <{vacancy.text[:20]}> - is not Python (not matched by LLM)")
        return False
