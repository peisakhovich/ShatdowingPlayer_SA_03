from __future__ import annotations

import json
from pathlib import Path

from ai.shadowing_pause import calculate_shadowing_pause


class ShadowingPlanBuilder:

    def __init__(
        self,
        *,
        phrase_code: str,
        phrase_locale: str,
        phrase_voice: str,
        phrase_voice_gender: str = "",

        translate_code: str,
        translate_locale: str,
        translate_voice: str,
        translate_voice_gender: str = "",

        speed: float = 1.0,
        repeat_count: int = 1,

        pause_factor: float = 1.0,
        pause_min: int = 500,
        pause_max: int = 5000,

        set_name: str = "Shadowing",
        set_description: str = "Generated shadowing session",
    ):
        self.phrase_code = phrase_code
        self.phrase_locale = phrase_locale
        self.phrase_voice = phrase_voice
        self.phrase_voice_gender = phrase_voice_gender

        self.translate_code = translate_code
        self.translate_locale = translate_locale
        self.translate_voice = translate_voice
        self.translate_voice_gender = translate_voice_gender

        self.speed = speed
        self.repeat_count = repeat_count

        self.pause_factor = pause_factor
        self.pause_min = pause_min
        self.pause_max = pause_max

        self.set_name = set_name
        self.set_description = set_description

    def build(
        self,
        segmentation_data: dict,
    ) -> dict:

        chunks = segmentation_data["chunks"]

        items = []

        for index, chunk in enumerate(
            chunks,
            start=1
        ):

            phrase_text = (
                chunk["text"].strip()
            )

            translate_text = (
                chunk["translation"].strip()
            )

            pause_ms = calculate_shadowing_pause(
                text=phrase_text,
                factor=self.pause_factor,
                min_pause=self.pause_min,
                max_pause=self.pause_max,
            )

            item = {
                "item_id": index,
                "item_order": index,

                "phrase_id": 0,
                "difficulty": 1,

                "phrase_text": phrase_text,
                "translate_text": translate_text,

                "phrase_code": self.phrase_code,
                "phrase_locale": self.phrase_locale,
                "phrase_voice": self.phrase_voice,
                "phrase_voice_gender": (
                    self.phrase_voice_gender
                ),

                "translate_code": self.translate_code,
                "language_level": chunk["language_level"],
                "translate_locale": self.translate_locale,
                "translate_voice": self.translate_voice,
                "translate_voice_gender": (
                    self.translate_voice_gender
                ),

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
    def save(
        data: dict,
        filename: str | Path,
    ) -> None:

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