from pydantic import BaseModel
from typing import List


class DefinitionEntity(BaseModel):
    definition: str
    language: str


class SynonymEntity(BaseModel):
    synonym: str
    language: str


class TranslationEntity(BaseModel):
    translation: str
    language: str


class ExampleEntity(BaseModel):
    example: str
    language: str


class WordEntity(BaseModel):
    word: str
    language: str
    definitions: List[DefinitionEntity] = []
    synonyms: List[SynonymEntity] = []
    translations: List[TranslationEntity] = []
    examples: List[ExampleEntity] = []

    def add_definition(self, definition: DefinitionEntity):
        self.definitions.append(definition)

    def add_synonym(self, synonym: SynonymEntity):
        self.synonyms.append(synonym)

    def add_translation(self, translation: TranslationEntity):
        self.translations.append(translation)

    def add_example(self, example: ExampleEntity):
        self.examples.append(example)
