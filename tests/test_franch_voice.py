import asyncio

import edge_tts


async def main():

    voices = await edge_tts.list_voices()

    print()
    print("French voices:")
    print("=" * 100)

    for voice in voices:

        if voice.get("Locale", "").lower().startswith("fr"):

            print(
                voice["ShortName"],
                "|",
                voice["Gender"],
                "|",
                voice["Locale"]
            )


if __name__ == "__main__":
    asyncio.run(main())