from __future__ import annotations

from ai.shadowing_segmenter import ShadowingSegmenter
from ai.shadowing_plan import ShadowingPlanBuilder


class ShadowingGenerator:

    def __init__(self, client=None):
        self.segmenter = ShadowingSegmenter(
            client=client
        )

    async def generate(
        self,
        *,
        text: str,

        source_language: str,
        target_language: str,

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
    ) -> dict:

        # --------------------------------------------------
        # AI segmentation + translation
        # --------------------------------------------------

        result = self.segmenter.segment(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )

        # --------------------------------------------------
        # Convert Pydantic model to plain dict
        # --------------------------------------------------

        segmentation_data = {
            "original_text": result.original_text,

            "chunks": [
                {
                    "text": chunk.text,
                    "translation": chunk.translation,
                    "ends_sentence": chunk.ends_sentence,
                }

                for chunk in result.chunks
            ],

            "total_chunks": result.total_chunks,
        }

        # --------------------------------------------------
        # Build session plan
        # --------------------------------------------------

        builder = ShadowingPlanBuilder(

            phrase_code=phrase_code,
            phrase_locale=phrase_locale,
            phrase_voice=phrase_voice,
            phrase_voice_gender=phrase_voice_gender,

            translate_code=translate_code,
            translate_locale=translate_locale,
            translate_voice=translate_voice,
            translate_voice_gender=translate_voice_gender,

            speed=speed,
            repeat_count=repeat_count,

            pause_factor=pause_factor,
            pause_min=pause_min,
            pause_max=pause_max,

            set_name=set_name,
            set_description=set_description,
        )

        plan = builder.build(
            segmentation_data
        )

        return plan