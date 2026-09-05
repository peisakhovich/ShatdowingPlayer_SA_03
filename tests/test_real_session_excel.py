from pathlib import Path
import asyncio

from session.session import Session
from session.session_excel import SessionExcel
from audio.tts import TTS


def test_export_real_plan_session():
    session_file = Path("data/cache/plan_session.json")
    output_file = Path("test_output/session_export.xlsx")

    assert session_file.exists(), (
        f"Не найден файл Session: {session_file}"
    )

    session = Session.load(session_file)

    # Получаем реальный справочник голосов Edge TTS.
    voices_raw = asyncio.run(
        TTS().get_voices()
    )

    # Приводим формат Edge TTS
    # к формату, который использует SessionExcel.
    voices = [
        {
            "short_name": voice.get("ShortName", ""),
            "locale": voice.get("Locale", ""),
            "locale_name": voice.get("LocaleName", ""),
            "gender": voice.get("Gender", ""),
            "friendly_name": voice.get("FriendlyName", ""),
        }
        for voice in voices_raw
    ]

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = SessionExcel.export(
        session,
        output_file,
        voices=voices,
    )

    assert result == output_file
    assert output_file.exists()

    print()
    print("Session:")
    print(f"  set_id:      {session.id}")
    print(f"  set_name:    {session.name}")
    print(f"  description: {session.description}")
    print(f"  items:       {len(session)}")

    print()
    print(f"TTS voices:   {len(voices)}")
    print(f"Excel created: {output_file}")