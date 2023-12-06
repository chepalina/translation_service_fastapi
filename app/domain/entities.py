from typing import List

from pydantic import BaseModel


class DefinitionEntity(BaseModel):
    definition: str
    language: str

    class Config:
        orm_mode = True
        from_attributes = True


class SynonymEntity(BaseModel):
    synonym: str
    language: str

    class Config:
        orm_mode = True
        from_attributes = True


class TranslationEntity(BaseModel):
    translation: str
    language: str

    class Config:
        orm_mode = True
        from_attributes = True


class ExampleEntity(BaseModel):
    example: str
    language: str

    class Config:
        orm_mode = True
        from_attributes = True


class WordEntity(BaseModel):
    word: str
    language: str
    definitions: List[DefinitionEntity] = []
    synonyms: List[SynonymEntity] = []
    translations: List[TranslationEntity] = []
    examples: List[ExampleEntity] = []

    class Config:
        orm_mode = True
        from_attributes = True

    def add_definition(self, definition: DefinitionEntity):
        self.definitions.append(definition)

    def add_synonym(self, synonym: SynonymEntity):
        self.synonyms.append(synonym)

    def add_translation(self, translation: TranslationEntity):
        self.translations.append(translation)

    def add_example(self, example: ExampleEntity):
        self.examples.append(example)
