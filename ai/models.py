"""
Sound Language Studio
---------------------

Module:
    ai.models

Purpose:
    Defines Pydantic data models used for language detection,
    text segmentation, and training-plan generation.

ru:
    Содержит модели Pydantic для определения языка,
    сегментации текста и генерации учебных планов.
"""
from pydantic import BaseModel


class DictationChunk(BaseModel):

    text: str

    language_level: str
    
    ends_sentence: bool


class DictationSegmentation(BaseModel):

    original_text: str

    chunks: list[DictationChunk]

    total_chunks: int


class ShadowingChunk(BaseModel):

    text: str

    translation: str

    language_level: str

    ends_sentence: bool


class ShadowingSegmentation(BaseModel):

    original_text: str

    chunks: list[ShadowingChunk]

    total_chunks: int


class DetectedLanguage(BaseModel):

    language_code: str