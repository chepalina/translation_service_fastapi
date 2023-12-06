from app.api.v1.schemas import WordSchema
from app.domain.entities import WordEntity


def map_word(word: WordEntity) -> WordSchema:
    return WordSchema(
        word=word.word,
        language=word.language,
        definitions=[d.definition for d in word.definitions],
        synonyms=[s.synonym for s in word.synonyms],
        translations=[t.translation for t in word.translations],
        examples=[e.example for e in word.examples],
    )
