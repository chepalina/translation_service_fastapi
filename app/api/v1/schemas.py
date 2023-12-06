from pydantic import BaseModel


class WordSchema(BaseModel):
    word: str
    language: str
    definitions: list[str] = []
    synonyms: list[str] = []
    translations: list[str] = []
    examples: list[str] = []
