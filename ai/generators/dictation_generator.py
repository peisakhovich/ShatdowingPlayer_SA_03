from __future__ import annotations

from ai.dictation_segmenter import DictationSegmenter
from ai.dictation_plan import DictationPlanBuilder


class DictationGenerator:
    """Генератор плана для сценария Dictation."""

    async def generate(
        self,
        *,
        text,
        scenario,
        phrase_code,
        phrase_locale,
        phrase_voice,
        phrase_voice_gender,
        repeat_count,
        pause_factor,
        user_language_level: str | None = None,
    ):
        # --------------------------------------------------
        # AI segmentation
        # --------------------------------------------------

        segmenter = DictationSegmenter()

        result = segmenter.segment(
            text
        )

        # --------------------------------------------------
        # Convert Pydantic model
        # --------------------------------------------------

        validated_data = {
            "original_text": result.original_text,

            "chunks": [
                {
                    "text": chunk.text,
                    "language_level": chunk.language_level,
                    "ends_sentence": chunk.ends_sentence,
                }

                for chunk in result.chunks
            ],

            "total_chunks": result.total_chunks,
        }

        # --------------------------------------------------
        # Build plan
        # --------------------------------------------------

        builder = DictationPlanBuilder(
            phrase_code=phrase_code,
            phrase_locale=phrase_locale,
            phrase_voice=phrase_voice,
            phrase_voice_gender=phrase_voice_gender,

            speed=1.0,
            repeat_count=repeat_count,

            pause_factor=pause_factor,

            set_name="Dictation",
            set_description="Generated dictation session",
        )

        plan = builder.build(
            validated_data
        )

        # --------------------------------------------------
        # Store scenario information
        # --------------------------------------------------

        plan["set"]["set_name"] = (
            f"Dictation - {scenario}"
        )

        return plan