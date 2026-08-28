from __future__ import annotations

from ai.models import ShadowingSegmentation
from ai.openai_client import OpenAIClient
from ai.shadowing_validator import ShadowingValidator



SHADOWING_PROMPT = """
You are a language teacher preparing a text for a shadowing exercise.

The provided text is written in the SOURCE LANGUAGE.

Your task is to divide the text into natural speech units suitable for shadowing.
Prefer complete sentences as the basic unit.
And provide a translation of each phrase into the TARGET LANGUAGE.

The original text must be preserved exactly.

Segmentation rules:

- The primary unit is a complete sentence.
- Keep each complete sentence as one chunk whenever reasonably possible.
- Do NOT split a sentence merely because it contains a comma.
- Do NOT split a sentence merely to keep chunks within a particular word count.
- Preserve natural grammatical and semantic structures.
- A sentence may be divided into multiple chunks only when it is unusually long
  or contains clearly separable large semantic structures.
- If a sentence must be divided, split it only at a natural grammatical
  or semantic boundary.
- Never create fragments that sound unnatural when spoken aloud.
- Keep the original order of the text.
- Preserve every word of the original text exactly.
- Do not rewrite, simplify, correct or paraphrase the source text.
- Do not add or remove words.

Translation rules:
- Translate every chunk completely.
- Preserve the meaning of the original phrase.
- Use natural language in the TARGET LANGUAGE.
- Do not translate word-by-word when this would produce unnatural language.
- Do not add explanations or comments.
- Do not omit information.
- Each source chunk must have exactly one translation.

Language level rules:
- Determine the CEFR language level of each chunk independently.
- Evaluate the level of the ORIGINAL SOURCE LANGUAGE phrase.
- Do NOT evaluate the difficulty of the translation.
- The level describes the language proficiency required to understand
  the vocabulary, grammar and meaning of the source phrase.
- Use only one of these CEFR levels:
  A1, A2, B1, B2, C1, C2.
- Do not use any other level or description.
- Do not determine one level for the entire text.
- Each chunk must have its own language level.

For each chunk provide:
- text: the exact original text;
- translation: translation of that exact chunk;
- language_level: the CEFR level of the source phrase;
- ends_sentence: whether the chunk ends a sentence.

Also provide:
- original_text: the original text exactly as provided;
- total_chunks: total number of chunks.

SOURCE LANGUAGE:
{source_language}

TARGET LANGUAGE:
{target_language}

TEXT:

{text}
"""




class ShadowingSegmenter:

    def __init__(self, client=None):

        self.client = client or OpenAIClient()

    def segment(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> ShadowingSegmentation:

        prompt = SHADOWING_PROMPT.format(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )

        result = self.client.ask_structured(
            prompt,
            ShadowingSegmentation
        )

        result.total_chunks = len(result.chunks)

        ShadowingValidator.validate(
            text,
            result
        )

        return result