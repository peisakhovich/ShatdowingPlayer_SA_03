"""
Sound Language Studio
---------------------

Подготовка набора для мобильного приложения с подробным progress reporting.
"""

import asyncio
from pathlib import Path
from typing import Callable

from api.client import ApiClient
from audio.cache import AudioCache
from audio.provider import AudioProvider
from audio.tts import TTS
from core.logger import logger


class MobileAudioError(Exception):
    """Ошибка подготовки набора для мобильного приложения."""


def _report_progress(callback, **values):
    if callback is None:
        return
    try:
        callback(dict(values))
    except Exception as error:
        # Ошибка UI callback не должна останавливать подготовку MP3.
        logger.warning(f"Mobile audio progress callback error: {error}")


def _raise_item_error(
    callback, *, index, total, si_id, phase,
    completed_steps, total_steps, error
):
    message = (
        f"Item {index}/{total}; si_id={si_id}; "
        f"Phase: {phase}; Error: {error}"
    )
    _report_progress(
        callback,
        status="error",
        item_index=index,
        items_total=total,
        si_id=si_id,
        phase=phase,
        completed_steps=completed_steps,
        total_steps=total_steps,
        percent=int(completed_steps * 100 / total_steps) if total_steps else 0,
        error=str(error),
    )
    raise MobileAudioError(message) from error


async def prepare_mobile_audio(
    api_client: ApiClient,
    set_id: int,
    progress_callback: Callable[[dict], None] | None = None,
) -> dict:
    """
    Подготавливает аудио выбранного набора для мобильного приложения.

    Callback вызывается из фонового потока и должен только сохранять
    полученный снимок прогресса, не обращаясь к Pygame.
    При ошибке finish_mobile_audio() не вызывается.
    """
    cache = AudioCache()
    tts = TTS()
    provider = AudioProvider(cache=cache, tts=tts)

    phase = "Loading items"
    _report_progress(
        progress_callback, status="running", item_index=0,
        items_total=0, si_id=None, phase=phase,
        completed_steps=0, total_steps=0, percent=0,
    )
    logger.info(f"Mobile audio: получение элементов набора {set_id}")

    try:
        response = await asyncio.to_thread(
            api_client.get_mobile_audio_items, set_id
        )
    except Exception as error:
        raise MobileAudioError(f"Phase: {phase}; Error: {error}") from error

    if not isinstance(response, dict):
        raise MobileAudioError(
            f"Phase: {phase}; API вернул ответ неожиданного формата."
        )

    items = response.get("items")
    if not isinstance(items, list) or not items:
        raise MobileAudioError(
            f"Phase: {phase}; В наборе {set_id} нет элементов для подготовки."
        )

    total = len(items)
    translation_steps = sum(
        1 for item in items
        if (
            isinstance(item, dict)
            and isinstance(item.get("translate_text"), str)
            and item.get("translate_text", "").strip()
            and isinstance(item.get("translate_voice"), str)
            and item.get("translate_voice", "").strip()
        )
    )
    # Phrase TTS и Upload обязательны для каждого элемента.
    # Translation TTS учитывается только при наличии текста и голоса.
    total_steps = total * 2 + translation_steps
    completed_steps = 0

    phase = "Starting mobile audio"
    _report_progress(
        progress_callback, status="running", item_index=0,
        items_total=total, si_id=None, phase=phase,
        completed_steps=0, total_steps=total_steps, percent=0,
    )
    try:
        await asyncio.to_thread(api_client.start_mobile_audio, set_id)
    except Exception as error:
        raise MobileAudioError(f"Phase: {phase}; Error: {error}") from error

    uploaded = 0

    for index, item in enumerate(items, start=1):
        si_id = item.get("si_id") if isinstance(item, dict) else None
        phase = "Validation"

        if not isinstance(item, dict):
            _raise_item_error(
                progress_callback, index=index, total=total, si_id=si_id,
                phase=phase, completed_steps=completed_steps,
                total_steps=total_steps, error="Invalid item data format.",
            )

        phrase_text = item.get("phrase_text")
        phrase_voice = item.get("phrase_voice")
        translate_text = item.get("translate_text")
        translate_voice = item.get("translate_voice")
        speed = item.get("speed")

        validation_error = None
        if si_id is None:
            validation_error = "Missing si_id."
        elif not isinstance(phrase_text, str) or not phrase_text.strip():
            validation_error = "Phrase text is missing."
        elif not isinstance(phrase_voice, str) or not phrase_voice.strip():
            validation_error = "Phrase voice is missing."
        else:
            try:
                speed = float(speed)
            except (TypeError, ValueError):
                validation_error = "Invalid playback speed."

        if validation_error:
            _raise_item_error(
                progress_callback, index=index, total=total, si_id=si_id,
                phase=phase, completed_steps=completed_steps,
                total_steps=total_steps, error=validation_error,
            )

        logger.info(f"Mobile audio: элемент {index}/{total}, si_id={si_id}")

        phase = "Phrase TTS"
        _report_progress(
            progress_callback, status="running", item_index=index,
            items_total=total, si_id=si_id, phase=phase,
            completed_steps=completed_steps, total_steps=total_steps,
            percent=int(completed_steps * 100 / total_steps),
        )
        try:
            phrase_path = await provider.get_audio(
                text=phrase_text, voice=phrase_voice, speed=speed
            )
            if not _valid_audio_file(phrase_path):
                raise MobileAudioError(
                    "AudioProvider returned an empty or missing phrase file."
                )
        except Exception as error:
            _raise_item_error(
                progress_callback, index=index, total=total, si_id=si_id,
                phase=phase, completed_steps=completed_steps,
                total_steps=total_steps, error=error,
            )

        completed_steps += 1
        _report_progress(
            progress_callback, status="running", item_index=index,
            items_total=total, si_id=si_id, phase=phase,
            completed_steps=completed_steps, total_steps=total_steps,
            percent=int(completed_steps * 100 / total_steps),
        )

        translate_path = None
        if isinstance(translate_text, str) and translate_text.strip():
            if isinstance(translate_voice, str) and translate_voice.strip():
                phase = "Translation TTS"
                _report_progress(
                    progress_callback, status="running", item_index=index,
                    items_total=total, si_id=si_id, phase=phase,
                    completed_steps=completed_steps, total_steps=total_steps,
                    percent=int(completed_steps * 100 / total_steps),
                )
                try:
                    translate_path = await provider.get_audio(
                        text=translate_text, voice=translate_voice, speed=speed
                    )
                    if not _valid_audio_file(translate_path):
                        raise MobileAudioError(
                            "AudioProvider returned an empty or missing translation file."
                        )
                except Exception as error:
                    _raise_item_error(
                        progress_callback, index=index, total=total, si_id=si_id,
                        phase=phase, completed_steps=completed_steps,
                        total_steps=total_steps, error=error,
                    )

                completed_steps += 1
                _report_progress(
                    progress_callback, status="running", item_index=index,
                    items_total=total, si_id=si_id, phase=phase,
                    completed_steps=completed_steps, total_steps=total_steps,
                    percent=int(completed_steps * 100 / total_steps),
                )
            else:
                logger.warning(
                    f"Mobile audio: у si_id={si_id} есть текст перевода, "
                    "но не указан голос перевода. Аудио перевода пропускается."
                )

        phase = "Upload"
        _report_progress(
            progress_callback, status="running", item_index=index,
            items_total=total, si_id=si_id, phase=phase,
            completed_steps=completed_steps, total_steps=total_steps,
            percent=int(completed_steps * 100 / total_steps),
        )
        try:
            await asyncio.to_thread(
                api_client.upload_mobile_audio_item,
                set_id,
                int(si_id),
                str(phrase_path),
                str(translate_path) if translate_path is not None else None,
            )
        except Exception as error:
            _raise_item_error(
                progress_callback, index=index, total=total, si_id=si_id,
                phase=phase, completed_steps=completed_steps,
                total_steps=total_steps, error=error,
            )

        completed_steps += 1
        uploaded += 1
        _report_progress(
            progress_callback, status="running", item_index=index,
            items_total=total, si_id=si_id, phase=phase,
            completed_steps=completed_steps, total_steps=total_steps,
            percent=int(completed_steps * 100 / total_steps),
        )

    phase = "Finishing mobile audio"
    _report_progress(
        progress_callback, status="running", item_index=total,
        items_total=total, si_id=None, phase=phase,
        completed_steps=completed_steps, total_steps=total_steps, percent=100,
    )
    try:
        await asyncio.to_thread(api_client.finish_mobile_audio, set_id)
    except Exception as error:
        raise MobileAudioError(f"Phase: {phase}; Error: {error}") from error

    logger.info(
        f"Mobile audio: набор {set_id} готов; загружено элементов: {uploaded}/{total}"
    )
    _report_progress(
        progress_callback, status="completed", item_index=total,
        items_total=total, si_id=None, phase="Completed",
        completed_steps=total_steps, total_steps=total_steps, percent=100,
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
