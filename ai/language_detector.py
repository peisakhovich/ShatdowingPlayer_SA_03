"""
Sound Language Studio
---------------------

Module:
    ai.language_detector

Purpose:
    Detects the language of input text using the OpenAI API and
    returns its ISO 639-1 language code.

ru:
    Определяет язык исходного текста с помощью OpenAI API
    и возвращает его двухбуквенный код ISO 639-1.
"""
from ai.models import DetectedLanguage
from ai.openai_client import OpenAIClient


LANGUAGE_DETECTION_PROMPT = """
Determine the language of the provided text.

Return only the ISO 639-1 two-letter language code.

Examples:
English -> en
Russian -> ru
Polish -> pl
German -> de
French -> fr
Spanish -> es
Italian -> it

Do not translate or modify the text.

TEXT:

{text}
"""

class LanguageDetector:

    def __init__(self, client=None):

        self.client = client or OpenAIClient()

    def detect(self, text):

        prompt = LANGUAGE_DETECTION_PROMPT.format(
            text=text
        )

        result = self.client.ask_structured(
            prompt,
            DetectedLanguage
        )

        return result.language_code.lower()