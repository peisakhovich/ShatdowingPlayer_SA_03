from pydantic import BaseModel


class DictationChunk(BaseModel):

    text: str

    ends_sentence: bool


class DictationSegmentation(BaseModel):

    original_text: str

    chunks: list[DictationChunk]

    total_chunks: int


class ShadowingChunk(BaseModel):

    text: str

    translation: str

    ends_sentence: bool


class ShadowingSegmentation(BaseModel):

    original_text: str

    chunks: list[ShadowingChunk]

    total_chunks: int


class DetectedLanguage(BaseModel):

    language_code: str