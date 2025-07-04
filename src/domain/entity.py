from dataclasses import dataclass
from datetime import datetime


@dataclass
class Vacancy:
    source: str
    title: str
    text: str
    publish_date: datetime

    def __repr__(self):
        return (f"Vacancy(source={self.source}, title={self.title}, text={self.text[:30]}, publish_dat"
                f"e={self.publish_date})")

    def to_html(self) -> str:
        """Конвертирует вакансию в HTML формат для Telegram"""
        date_str = self.publish_date.strftime("%Y-%m-%d %H:%M")

        html = [
            f"<b>{self.title}</b>",
            f"<i>Источник: {self.source}</i>",
            f"<i>Дата: {date_str}</i>",
            "",
            self.text
        ]

        return "\n".join(html)
