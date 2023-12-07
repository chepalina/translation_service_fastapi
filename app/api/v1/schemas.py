from typing import Optional

from pydantic import BaseModel


class DefinitionSchema(BaseModel):
    definition: str


class SynonymSchema(BaseModel):
    synonym: str


class TranslationSchema(BaseModel):
    translation: str


class ExampleSchema(BaseModel):
    example: str


class WordSchema(BaseModel):
    word: str
    language: str

    definitions: Optional[list[DefinitionSchema]] = None
    synonyms: Optional[list[SynonymSchema]] = None
    translations: Optional[list[TranslationSchema]] = None
    examples: Optional[list[ExampleSchema]] = None
