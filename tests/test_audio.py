import asyncio

from audio.cache import AudioCache
from audio.tts import TTS


async def test_tts_cache():

    cache = AudioCache("data/audio_cache")
    tts = TTS()

    text = "To jest test pamięci podręcznej."
    voice = "pl-PL-ZofiaNeural"
    speed = 0.6

    path = cache.get_path(
        text=text,
        voice=voice,
        speed=speed,
    )

    print(f"Cache path: {path}")

    if cache.exists(
        text=text,
        voice=voice,
        speed=speed,
    ):
        print("CACHE HIT")
        print("TTS не вызываем")

    else:
        print("CACHE MISS")
        print("Вызываем TTS...")

        await tts.synthesize(
            text=text,
            voice=voice,
            speed=speed,
            output_path=path,
        )

        print("TTS завершён")


if __name__ == "__main__":
    asyncio.run(test_tts_cache())