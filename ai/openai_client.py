"""
Sound Language Studio
---------------------

Module:
    ai.openai_client

Purpose:
    Provides a small wrapper around the OpenAI API for text generation
    and structured responses.

ru:
    Предоставляет простой интерфейс для работы с OpenAI API,
    включая генерацию текста и структурированных ответов.
"""
from openai import OpenAI


class OpenAIClient:

    def __init__(self):
        self.client = OpenAI()

    def ask(self, prompt):
        response = self.client.responses.create(
            model="gpt-5.6",
            input=prompt
        )

        return response.output_text

    def ask_structured(self, prompt, schema):
        response = self.client.responses.parse(
            model="gpt-5.6",
            input=prompt,
            text_format=schema
        )

        return response.output_parsed