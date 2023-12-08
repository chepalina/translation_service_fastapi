from typing import List, Optional

import strawberry


@strawberry.type
class DefinitionType:
    language: str
    definition: str


@strawberry.type
class SynonymType:
    language: str
    synonym: str


@strawberry.type
class TranslationType:
    language: str
    translation: str


@strawberry.type
class ExampleType:
    language: str
    example: str


@strawberry.type
class WordType:
    word: str
    language: str

    # Relationships
    definitions: Optional[List[DefinitionType]] = None
    synonyms: Optional[List[SynonymType]] = None
    translations: Optional[List[TranslationType]] = None
    examples: Optional[List[ExampleType]] = None
