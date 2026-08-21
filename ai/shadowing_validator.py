from __future__ import annotations

import re

from ai.models import ShadowingSegmentation


class ShadowingValidator:
    """Проверяет результат ShadowingSegmenter."""

    @staticmethod
    def _normalize(text: str) -> str:

        text = text.lower()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    @classmethod
    def validate(
        cls,
        original_text: str,
        result: ShadowingSegmentation,
    ) -> None:

        # --------------------------------------------------
        # Original text
        # --------------------------------------------------

        original = cls._normalize(
            original_text
        )

        returned_original = cls._normalize(
            result.original_text
        )

        if original != returned_original:

            raise ValueError(
                "Shadowing validation failed: "
                "original_text was modified."
            )

        # --------------------------------------------------
        # Chunks
        # --------------------------------------------------

        if not result.chunks:

            raise ValueError(
                "Shadowing validation failed: "
                "no chunks returned."
            )

        # --------------------------------------------------
        # Total chunks
        # --------------------------------------------------

        if result.total_chunks != len(
            result.chunks
        ):

            raise ValueError(
                "Shadowing validation failed: "
                "total_chunks does not match "
                "the number of chunks."
            )

        # --------------------------------------------------
        # Validate individual chunks
        # --------------------------------------------------

        chunk_texts = []

        for index, chunk in enumerate(
            result.chunks,
            start=1
        ):

            text = chunk.text.strip()

            translation = (
                chunk.translation.strip()
            )

            if not text:

                raise ValueError(
                    f"Shadowing validation failed: "
                    f"chunk {index} has empty text."
                )

            if not translation:

                raise ValueError(
                    f"Shadowing validation failed: "
                    f"chunk {index} has empty translation."
                )

            chunk_texts.append(text)

        # --------------------------------------------------
        # Reconstruct original text
        # --------------------------------------------------

        reconstructed = cls._normalize(
            " ".join(chunk_texts)
        )

        # --------------------------------------------------
        # Compare source and reconstructed text
        # --------------------------------------------------

        if reconstructed != original:

            raise ValueError(
                "Shadowing validation failed: "
                "chunks do not preserve the "
                "original text."
            )