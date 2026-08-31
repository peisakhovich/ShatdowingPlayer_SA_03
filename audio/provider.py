
from pathlib import Path
import tempfile

from audio.cache import AudioCache
from audio.tts import TTS
from core.logger import logger


class AudioProvider:
    """Предоставляет готовые аудиофайлы."""

    def __init__(
        self,
        cache: AudioCache,
        tts: TTS,
    ):
        self.cache = cache
        self.tts = tts

    async def get_audio(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> Path:
        """Возвращает путь к готовому MP3."""

        # -----------------------------------------------------
        # Проверяем кэш
        # -----------------------------------------------------

        path = self.cache.get_path(
            text=text,
            voice=voice,
            speed=speed,
        )

        if self.cache.exists(
            text=text,
            voice=voice,
            speed=speed,
        ):
            logger.debug("AudioProvider: CACHE HIT")
            return path

        # -----------------------------------------------------
        # Генерация нового аудио
        # -----------------------------------------------------

        # -----------------------------------------------------
        # Проверка необходимости генерации
        # -----------------------------------------------------

        if not text or not voice:
            return None

        logger.debug("AudioProvider: CACHE MISS")
   
        # TTS пишет во временный файл.
        # Финальный файл кэша до успешного завершения
        # генерации не существует.
        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False,
        ) as temp_file:

            temp_path = Path(temp_file.name)

        try:

            await self.tts.synthesize(
                text=text,
                voice=voice,
                speed=speed,
                output_path=temp_path,
            )

            # Только после успешной генерации
            # сохраняем MP3 в постоянный кэш.
            path = self.cache.save(
                source_path=temp_path,
                text=text,
                voice=voice,
                speed=speed,
            )

            return path

        except Exception as e:

            logger.warning(
                f"AudioProvider: TTS failed: {e}"
            )

            return None

        finally:

            # Временный файл удаляется как после успешной,
            # так и после отменённой/неудачной генерации.
            if temp_path.exists():
                temp_path.unlink()

