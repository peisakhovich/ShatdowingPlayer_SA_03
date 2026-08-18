import re

from ai.models import DictationSegmentation


class DictationValidationError(Exception):
    pass


class DictationValidator:

    @staticmethod
    def normalize_text(text):
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def validate(
        source_text: str,
        result: DictationSegmentation
    ):
        # ----------------------------------------
        # 1. Проверяем original_text
        # ----------------------------------------

        if DictationValidator.normalize_text(
            result.original_text
        ) != DictationValidator.normalize_text(
            source_text
        ):
            raise DictationValidationError(
                "GPT changed the original text."
            )

        # ----------------------------------------
        # 2. Проверяем количество chunks
        # ----------------------------------------

        if result.total_chunks != len(result.chunks):
            raise DictationValidationError(
                "total_chunks does not match the actual number of chunks."
            )

        # ----------------------------------------
        # 3. Проверяем chunks
        # ----------------------------------------

        for index, chunk in enumerate(result.chunks):

            if not chunk.text.strip():
                raise DictationValidationError(
                    f"Chunk {index} is empty."
                )

        # ----------------------------------------
        # 4. Восстанавливаем текст
        # ----------------------------------------

        reconstructed_text = " ".join(
            chunk.text.strip()
            for chunk in result.chunks
        )

        # ----------------------------------------
        # 5. Проверяем сохранность текста
        # ----------------------------------------

        if DictationValidator.normalize_text(
            reconstructed_text
        ) != DictationValidator.normalize_text(
            source_text
        ):
            raise DictationValidationError(
                "Chunks do not reconstruct the original text."
            )

        return True