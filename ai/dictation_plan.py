from __future__ import annotations

import json
from pathlib import Path

from ai.dictation_pause import calculate_dictation_pause


class DictationPlanBuilder:

    def __init__(
        self,
        *,
        phrase_code: str,
        phrase_locale: str,
        phrase_voice: str,
        phrase_voice_gender: str = "",
        speed: float = 1.0,
        repeat_count: int = 1,
        pause_factor: float = 2.0,
        pause_min: int = 300,
        pause_max: int = 10000,
        set_name: str = "Dictation",
        set_description: str = "Generated dictation session",
    ):
        self.phrase_code = phrase_code
        self.phrase_locale = phrase_locale
        self.phrase_voice = phrase_voice
        self.phrase_voice_gender = phrase_voice_gender

        self.speed = speed
        self.repeat_count = repeat_count

        self.pause_factor = pause_factor
        self.pause_min = pause_min
        self.pause_max = pause_max

        self.set_name = set_name
        self.set_description = set_description

    def build(self, validated_data: dict) -> dict:

        chunks = validated_data["chunks"]

        items = []

        for index, chunk in enumerate(chunks, start=1):

            text = chunk["text"]

            pause_ms = calculate_dictation_pause(
                text=text,
                factor=self.pause_factor,
                min_pause=self.pause_min,
                max_pause=self.pause_max,
            )

            item = {
                "item_id": index,
                "item_order": index,
                "phrase_id": 0,
                "difficulty": 1,

                "phrase_text": text,
                "translate_text": "",

                "phrase_code": self.phrase_code,
                "phrase_locale": self.phrase_locale,
                "phrase_voice": self.phrase_voice,
                "phrase_voice_gender": self.phrase_voice_gender,

                "translate_code": "",
                "translate_locale": "",
                "translate_voice": "",
                "translate_voice_gender": "",

                "pause_ms": pause_ms,
                "speed": self.speed,
                "repeat_count": self.repeat_count,
            }

            items.append(item)

        return {
            "set": {
                "set_id": 0,
                "user_id": 0,
                "user_nickname": "guest",

                "set_index": 1,

                "set_name": self.set_name,
                "set_description": self.set_description,

                "set_active": True,

                "set_create_date": "",

                "items_count": len(items),
            },

            "items": items,

            "state": {
                "current_index": 0
            }
        }

    @staticmethod
    def save(data: dict, filename: str | Path) -> None:

        filename = Path(filename)

        filename.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )