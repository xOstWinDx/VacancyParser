import logging
import re
import unicodedata

from yandex_cloud_ml_sdk import YCloudML

from src.config import settings
from src.domain.entity import Vacancy
from src.interfaces.validator import AbstractVacancyValidator


class TestVacancyValidator(AbstractVacancyValidator):
    def validate(self, vacancy: Vacancy) -> bool:
        return True


class YandexVacancyValidator(AbstractVacancyValidator):
    python_pattern = re.compile(r'\b(python\s?\d*\.?\d*|py\s?\d*\.?\d*|питон|пайтон)\b', re.IGNORECASE)
    framework_pattern = re.compile(r'\b(fastapi|django|flask)\b', re.IGNORECASE)
    exclude_pattern = re.compile(
        r'\b(java(script)?|js|c\#|1с|1c|frontend|фронтенд|front[\s\-]?end|'
        r'react|angular|vue|data\s*science|datascience|pandas|numpy|tensorflow|'
        r'machine\s*learning|ml|аналитик|ai)\b',
        re.IGNORECASE
    )

    @staticmethod
    def normalize_text(text: str) -> str:
        normalized = unicodedata.normalize("NFKC", text)
        return normalized.lower().strip()

    def validate(self, vacancy: Vacancy) -> bool:
        cleaned = self.normalize_text(vacancy.text)
        if not (
                self.python_pattern.search(cleaned) and
                self.framework_pattern.search(cleaned) and
                not self.exclude_pattern.search(cleaned)
        ):
            logging.info(f"Vacancy {vacancy} is invalid by regex")
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
            logging.info(f"Vacancy: {vacancy} - valid!")
            return True
        logging.info(f"Vacancy {vacancy} is invalid by LLM")
        return False
