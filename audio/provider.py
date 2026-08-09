from pathlib import Path

from audio.cache import AudioCache
from audio.tts import TTS


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
            print("AudioProvider: CACHE HIT")
            return path

        print("AudioProvider: CACHE MISS")
        print("AudioProvider: generating TTS...")

        await self.tts.synthesize(
            text=text,
            voice=voice,
            speed=speed,
            output_path=path,
        )

        return path