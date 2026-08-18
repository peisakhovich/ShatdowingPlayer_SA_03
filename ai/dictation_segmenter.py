from ai.models import DictationSegmentation
from ai.openai_client import OpenAIClient
from ai.dictation_validator import DictationValidator


DICTATION_PROMPT = """
You are a language teacher preparing a text for a dictation exercise
in the language of the provided text.

Your task is to segment the given text into natural, meaningful chunks
that a teacher could dictate to a student.

The student should first hear the entire text once.

Then the text is dictated chunk by chunk.

For each chunk:
1. The teacher reads the chunk naturally.
2. The student gets time to write it down.
3. The teacher repeats the chunk once.
4. The exercise continues with the next chunk.

Segmentation rules:
- Preserve the original text exactly. Do not rewrite, simplify or correct it.
- Do not split phrases in places that destroy their meaning.
- Prefer natural grammatical and semantic boundaries.
- A chunk should normally contain approximately 4–10 words.
- A chunk may be shorter or longer when necessary to preserve a natural phrase.
- Use punctuation and grammatical structure as important clues for segmentation.
- Avoid creating very short fragments such as "because", "at work", "the bus", etc.
- A complete short sentence may remain a single chunk.
- A long sentence may be divided into several meaningful chunks.
- Keep the original order of the text.

For each chunk, provide:
- the exact text;
- whether the chunk ends a sentence.

Also provide:
- the original text;
- the total number of chunks.

TEXT:

{text}
"""


class DictationSegmenter:

    def __init__(self, client=None):
        self.client = client or OpenAIClient()

    def segment(self, text):
        prompt = DICTATION_PROMPT.format(text=text)

        result = self.client.ask_structured(
            prompt,
            DictationSegmentation
        )

        DictationValidator.validate(text, result)

        return result