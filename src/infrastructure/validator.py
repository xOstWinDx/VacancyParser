from yandex_cloud_ml_sdk import YCloudML

from src.config import settings
from src.domain.entity import Vacancy
from src.interfaces.validator import AbstractVacancyValidator


class TestVacancyValidator(AbstractVacancyValidator):
    def validate(self, vacancy: Vacancy) -> bool:
        return True


class YandexVacancyValidator(AbstractVacancyValidator):

    def validate(self, vacancy: Vacancy) -> bool:
        messages = [
            {
                "role": "system",
                "text": """
                    Ты — анализатор вакансий. Чётко следуй правилам:
                    Вакансия подходит, если ВСЕ условия выполнены:

                    Должность: Python-бэкенд (если не указано — не подходит)

                    Технологии: Требуется FastAPI

                    Формат: Удалёнка или не указано

                    Уровень: Мидл/Джуниор/Не указан (если Senior — не подходит)

                    Если ВСЕ условия выше выполнены — отвечай "Yes"

                    Если ХОТЯ БЫ ОДНО условие не выполнено — отвечай "No"

                    Никаких других слов в ответе не должно быть, только "Yes" или "No"
                    Не обьясняй почему ответ такой, пиши только сам ответ и всё.
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

        result = sdk.models.completions("llama-lite", model_version="latest").configure(temperature=0.5).run(messages)

        assert len(result) == 1
        return result[0].text.strip() == "Yes"