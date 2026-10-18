"""
Sound Language Studio
---------------------

Подготовка набора для мобильного приложения:
1. Получение списка элементов с API.
2. Получение или генерация MP3 через AudioProvider.
3. Загрузка аудио каждого элемента.
4. Подтверждение готовности набора на сервере.

Важно:
Сервер получает статус готовности только после успешной
обработки и загрузки всех элементов набора.
"""

import asyncio
from pathlib import Path

from api.client import ApiClient
from audio.cache import AudioCache
from audio.provider import AudioProvider
from audio.tts import TTS
from core.logger import logger


class MobileAudioError(Exception):
    """Ошибка подготовки набора для мобильного приложения."""


async def prepare_mobile_audio(
    api_client: ApiClient,
    set_id: int,
) -> dict:
    """
    Подготавливает аудио выбранного набора для мобильного приложения.

    Возвращает сводку о количестве обработанных элементов.
    При ошибке не вызывает finish_mobile_audio().
    """

    cache = AudioCache()
    tts = TTS()
    provider = AudioProvider(cache=cache, tts=tts)

    logger.info(
        f"Mobile audio: получение элементов набора {set_id}"
    )

    # Сначала получаем список элементов.
    # При ошибке пока не меняем статус готовности набора на сервере.
    response = await asyncio.to_thread(
        api_client.get_mobile_audio_items,
        set_id,
    )

    if not isinstance(response, dict):
        raise MobileAudioError(
            "API вернул ответ неожиданного формата."
        )

    items = response.get("items")

    if not isinstance(items, list) or not items:
        raise MobileAudioError(
            f"В наборе {set_id} нет элементов для подготовки."
        )

    # Начинаем подготовку на сервере.
    await asyncio.to_thread(
        api_client.start_mobile_audio,
        set_id,
    )

    total = len(items)
    uploaded = 0

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise MobileAudioError(
                f"Элемент №{index}: неверный формат данных."
            )

        si_id = item.get("si_id")
        phrase_text = item.get("phrase_text")
        phrase_voice = item.get("phrase_voice")
        translate_text = item.get("translate_text")
        translate_voice = item.get("translate_voice")
        speed = item.get("speed")

        if si_id is None:
            raise MobileAudioError(
                f"Элемент №{index}: отсутствует si_id."
            )

        if not isinstance(phrase_text, str) or not phrase_text.strip():
            raise MobileAudioError(
                f"Элемент si_id={si_id}: отсутствует текст фразы."
            )

        if not isinstance(phrase_voice, str) or not phrase_voice.strip():
            raise MobileAudioError(
                f"Элемент si_id={si_id}: отсутствует голос фразы."
            )

        try:
            speed = float(speed)
        except (TypeError, ValueError):
            raise MobileAudioError(
                f"Элемент si_id={si_id}: некорректная скорость."
            ) from None

        logger.info(
            f"Mobile audio: элемент {index}/{total}, si_id={si_id}"
        )

        # Получаем MP3 фразы из кэша или генерируем через TTS.
        phrase_path = await provider.get_audio(
            text=phrase_text,
            voice=phrase_voice,
            speed=speed,
        )

        if not _valid_audio_file(phrase_path):
            raise MobileAudioError(
                f"Не удалось получить аудио фразы si_id={si_id}."
            )

        translate_path = None

        # Перевод необязателен.
        # Если текст есть и голос задан, готовим аудио перевода.
        if isinstance(translate_text, str) and translate_text.strip():
            if (
                isinstance(translate_voice, str)
                and translate_voice.strip()
            ):
                translate_path = await provider.get_audio(
                    text=translate_text,
                    voice=translate_voice,
                    speed=speed,
                )

                if not _valid_audio_file(translate_path):
                    raise MobileAudioError(
                        "Не удалось получить аудио перевода "
                        f"si_id={si_id}."
                    )
            else:
                logger.warning(
                    f"Mobile audio: у si_id={si_id} есть текст перевода, "
                    "но не указан голос перевода. "
                    "Аудио перевода пропускается."
                )

        # Загружаем аудио по si_id, а не по порядковому номеру.
        await asyncio.to_thread(
            api_client.upload_mobile_audio_item,
            set_id,
            int(si_id),
            str(phrase_path),
            (
                str(translate_path)
                if translate_path is not None
                else None
            ),
        )

        uploaded += 1

    # Завершаем подготовку только после успешной загрузки всех элементов.
    await asyncio.to_thread(
        api_client.finish_mobile_audio,
        set_id,
    )

    logger.info(
        f"Mobile audio: набор {set_id} готов; "
        f"загружено элементов: {uploaded}/{total}"
    )

    return {
        "set_id": set_id,
        "items_total": total,
        "items_uploaded": uploaded,
    }


def _valid_audio_file(path: Path | None) -> bool:
    """Проверяет, что файл существует и не пуст."""

    if path is None:
        return False

    try:
        return path.is_file() and path.stat().st_size > 0
    except OSError:
        return False