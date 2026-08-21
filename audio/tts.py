import edge_tts


class TTS:
    """Генератор аудио и справочник голосов Edge TTS."""

    async def get_voices(self):
        """Возвращает все доступные голоса Edge TTS."""
        return await edge_tts.list_voices()

    async def get_voices_for_language(self, language: str):
        """
        Возвращает голоса для указанного языка.

        language:
            двухбуквенный код языка, например:
            en, pl, ru
        """

        if not language:
            return []

        language = language.lower()

        voices = await self.get_voices()

        result = []

        for voice in voices:

            locale = voice.get("Locale", "")

            if not locale:
                continue

            voice_language = locale.split("-")[0].lower()

            if voice_language != language:
                continue

            result.append({
                "short_name": voice.get("ShortName", ""),
                "locale": locale,
                "locale_name": voice.get("LocaleName", ""),
                "gender": voice.get("Gender", ""),
                "friendly_name": voice.get("FriendlyName", ""),
            })

        return result

    async def get_locales_for_language(self, language: str):
        """
        Возвращает список locale для указанного языка.

        Например:
            en -> ["en-AU", "en-CA", ...]
            pl -> ["pl-PL"]
            ru -> ["ru-RU"]
        """

        if not language:
            return []

        language = language.lower()

        voices = await self.get_voices()

        locales = set()

        for voice in voices:

            locale = voice.get("Locale", "")

            if not locale:
                continue

            voice_language = locale.split("-")[0].lower()

            if voice_language == language:
                locales.add(locale)

        return sorted(locales)

    async def get_voices_for_locale(self, locale: str):
        """
        Возвращает голоса для указанного locale.
        """

        if not locale:
            return []

        voices = await self.get_voices()

        result = []

        for voice in voices:

            if voice.get("Locale", "") != locale:
                continue

            result.append({
                "short_name": voice.get("ShortName", ""),
                "locale": voice.get("Locale", ""),
                "locale_name": voice.get("LocaleName", ""),
                "gender": voice.get("Gender", ""),
                "friendly_name": voice.get("FriendlyName", ""),
            })

        return result




    async def synthesize(
        self,
        text: str,
        voice: str,
        speed: float,
        output_path: str,
    ):
        """Генерирует MP3 для заданного текста и голоса."""

        if not text or not voice:
            return

        rate_value = (speed - 1) * 100
        rate_str = f"{rate_value:+.0f}%"

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate_str,
        )

        await communicate.save(output_path)

    async def get_languages(self):
        """Возвращает список доступных двухбуквенных кодов языков."""

        voices = await self.get_voices()

        languages = set()

        for voice in voices:

            locale = voice.get("Locale", "")

            if not locale:
                continue

            language = locale.split("-")[0].lower()

            languages.add(language)

        return sorted(languages)        