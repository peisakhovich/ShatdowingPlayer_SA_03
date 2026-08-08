from pathlib import Path
import hashlib
import shutil


class AudioCache:
    """Хранилище сгенерированных аудиофайлов."""

    SPEED_STEP = 0.1

    def __init__(self, cache_dir="data/audio_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _normalize_speed(self, speed: float) -> float:
        """Округляет скорость до ближайшего шага 0.1."""

        return round(speed / self.SPEED_STEP) * self.SPEED_STEP

    def _make_key(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> str:
        """Создаёт уникальный ключ для text + voice + speed."""

        speed = self._normalize_speed(speed)

        source = f"{voice}:{speed}:{text}"

        return hashlib.sha256(
            source.encode("utf-8")
        ).hexdigest()

    def get_path(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> Path:
        """Возвращает путь к mp3 для text + voice + speed."""

        key = self._make_key(
            text,
            voice,
            speed,
        )

        return self.cache_dir / f"{key}.mp3"

    def exists(
        self,
        text: str,
        voice: str,
        speed: float,
    ) -> bool:
        """Проверяет наличие аудио в кэше."""

        return self.get_path(
            text,
            voice,
            speed,
        ).exists()

    def save(
        self,
        source_path: str | Path,
        text: str,
        voice: str,
        speed: float,
    ) -> Path:
        """Сохраняет готовый MP3 в кэш."""

        source_path = Path(source_path)

        target_path = self.get_path(
            text,
            voice,
            speed,
        )

        shutil.copy2(
            source_path,
            target_path,
        )

        return target_path