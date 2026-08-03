"""
guest_provider.py

Создает тестовую сессию приложения SA_03.

Используется только при первом запуске, когда файл
plan_session.json отсутствует.

После появления SqlProvider будет заменен без изменения
остальной архитектуры приложения.
"""

from __future__ import annotations

import json
from pathlib import Path


class GuestProvider:

    @staticmethod
    def build(filename: str | Path) -> None:
        """
        Создать файл plan_session.json с тестовыми данными.
        """

        filename = Path(filename)

        # Создаем каталог при необходимости
        filename.parent.mkdir(parents=True, exist_ok=True)

        data = {

            "set": {

                "set_id": 0,
                "user_id": 0,
                "user_nickname": "guest",

                "set_index": 1,

                "set_name": "Guest Session",
                "set_description": "Automatically generated test session",

                "set_active": True,

                "set_create_date": "",

                "items_count": 5
            },

            "items": [

                {
                    "item_id": 1,
                    "item_order": 1,
                    "phrase_id": 1,
                    "difficulty": 1,

                    "phrase_text": "Good morning.",
                    "translate_text": "Доброе утро.",

                    "phrase_code": "en",
                    "phrase_locale": "en-US",
                    "phrase_voice": "en-US-JennyNeural",
                    "phrase_voice_gender": "Female",

                    "translate_code": "ru",
                    "translate_locale": "ru-RU",
                    "translate_voice": "ru-RU-SvetlanaNeural",
                    "translate_voice_gender": "Female",

                    "pause_ms": 2000,
                    "speed": 1.00,
                    "repeat_count": 1
                },

                {
                    "item_id": 2,
                    "item_order": 2,
                    "phrase_id": 2,
                    "difficulty": 1,

                    "phrase_text": "How are you?",
                    "translate_text": "Как дела?",

                    "phrase_code": "en",
                    "phrase_locale": "en-US",
                    "phrase_voice": "en-US-JennyNeural",
                    "phrase_voice_gender": "Female",

                    "translate_code": "ru",
                    "translate_locale": "ru-RU",
                    "translate_voice": "ru-RU-SvetlanaNeural",
                    "translate_voice_gender": "Female",

                    "pause_ms": 2000,
                    "speed": 1.00,
                    "repeat_count": 1
                },

                {
                    "item_id": 3,
                    "item_order": 3,
                    "phrase_id": 3,
                    "difficulty": 1,

                    "phrase_text": "My name is John.",
                    "translate_text": "Меня зовут Джон.",

                    "phrase_code": "en",
                    "phrase_locale": "en-US",
                    "phrase_voice": "en-US-JennyNeural",
                    "phrase_voice_gender": "Female",

                    "translate_code": "ru",
                    "translate_locale": "ru-RU",
                    "translate_voice": "ru-RU-SvetlanaNeural",
                    "translate_voice_gender": "Female",

                    "pause_ms": 2000,
                    "speed": 1.00,
                    "repeat_count": 1
                },

                {
                    "item_id": 4,
                    "item_order": 4,
                    "phrase_id": 4,
                    "difficulty": 1,

                    "phrase_text": "See you tomorrow.",
                    "translate_text": "До встречи завтра.",

                    "phrase_code": "en",
                    "phrase_locale": "en-US",
                    "phrase_voice": "en-US-JennyNeural",
                    "phrase_voice_gender": "Female",

                    "translate_code": "ru",
                    "translate_locale": "ru-RU",
                    "translate_voice": "ru-RU-SvetlanaNeural",
                    "translate_voice_gender": "Female",

                    "pause_ms": 2000,
                    "speed": 1.00,
                    "repeat_count": 1
                },

                {
                    "item_id": 5,
                    "item_order": 5,
                    "phrase_id": 5,
                    "difficulty": 1,

                    "phrase_text": "Thank you very much.",
                    "translate_text": "Большое спасибо.",

                    "phrase_code": "en",
                    "phrase_locale": "en-US",
                    "phrase_voice": "en-US-JennyNeural",
                    "phrase_voice_gender": "Female",

                    "translate_code": "ru",
                    "translate_locale": "ru-RU",
                    "translate_voice": "ru-RU-SvetlanaNeural",
                    "translate_voice_gender": "Female",

                    "pause_ms": 2000,
                    "speed": 1.00,
                    "repeat_count": 1
                }

            ],

            "state": {

                "current_index": 0

            }

        }

        with open(filename, "w", encoding="utf-8") as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

        print(f"Guest session created: {filename}")