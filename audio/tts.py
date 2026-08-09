import edge_tts


class TTS:
    """Генератор аудио через Edge TTS."""

    async def synthesize(
        self,
        text: str,
        voice: str,
        speed: float,
        output_path: str,
    ):
        """Генерирует MP3 для заданного текста, голоса и скорости."""

        rate_value = (speed - 1) * 100
        rate_str = f"{rate_value:+.0f}%"

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate_str,
        )

        await communicate.save(output_path)