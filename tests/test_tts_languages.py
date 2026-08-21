import asyncio

from audio.tts import TTS


async def main():

    tts = TTS()

    languages = await tts.get_languages()

    print()
    print("==============================")
    print("TTS LANGUAGES")
    print("==============================")

    print(
        "Count:",
        len(languages)
    )

    print("------------------------------")

    for language in languages:

        print(
            language
        )

    print("==============================")
    print()


if __name__ == "__main__":

    asyncio.run(
        main()
    )