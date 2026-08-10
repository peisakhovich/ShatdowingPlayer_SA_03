import asyncio
import time

from audio.cache import AudioCache
from audio.tts import TTS
from audio.provider import AudioProvider
from audio.mixer import AudioMixer


async def test_provider_mixer():

    cache = AudioCache("data/audio_cache")
    tts = TTS()

    provider = AudioProvider(
        cache=cache,
        tts=tts,
    )

    mixer = AudioMixer()

    path = await provider.get_audio(
        text="To jest test pełnego cyklu audio.",
        voice="pl-PL-ZofiaNeural",
        speed=0.6,
    )

    print(f"Audio path: {path}")
    print(f"Exists: {path.exists()}")

    mixer.load(path)

    print("Playing...")
    mixer.play()

    while mixer.is_playing():
        time.sleep(0.1)

    print("Playback finished")


if __name__ == "__main__":
    asyncio.run(test_provider_mixer())