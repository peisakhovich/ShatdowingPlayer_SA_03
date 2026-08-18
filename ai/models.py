from pydantic import BaseModel


class DictationChunk(BaseModel):
    text: str
    ends_sentence: bool


class DictationSegmentation(BaseModel):
    original_text: str
    chunks: list[DictationChunk]
    total_chunks: int