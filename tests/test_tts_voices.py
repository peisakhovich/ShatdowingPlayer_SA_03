import asyncio

from audio.tts import TTS


async def main():

    tts = TTS()

    for language in ("en", "pl", "ru"):

        print()
        print("=" * 50)
        print(f"LANGUAGE: {language}")

        locales = await tts.get_locales_for_language(language)

        print(f"Locales: {len(locales)}")

        for locale in locales:

            voices = await tts.get_voices_for_locale(locale)

            print()
            print(f"  {locale}: {len(voices)} voices")

            for voice in voices:

                print(
                    f"    {voice['short_name']} | "
                    f"{voice['gender']}"
                )


if __name__ == "__main__":
    asyncio.run(main())