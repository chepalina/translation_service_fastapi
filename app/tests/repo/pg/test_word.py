import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Definition as DefinitionModel
from app.models import Example as ExampleModel
from app.models import Synonym as SynonymModel
from app.models import Translation as TranslationModel
from app.models import Word as WordModel
from app.repo.pg.word import UndefinedWordException, WordPgRepo


async def test_get_word(session: AsyncSession):

    # Setup test data
    test_word = WordModel(word="apple", language="en")
    test_definition = DefinitionModel(
        definition="A fruit", language="en", word=test_word
    )
    test_synonym = SynonymModel(synonym="pome", language="en", word=test_word)
    test_translation = TranslationModel(
        translation="manzana", language="es", word=test_word
    )
    test_example = ExampleModel(
        example="An apple a day keeps the doctor away.", language="en", word=test_word
    )

    session.add_all(
        [test_word, test_definition, test_synonym, test_translation, test_example]
    )
    await session.commit()

    # Instantiate the repository with the test session
    repo = WordPgRepo(_session_factory=lambda: session)

    # Test the get method
    word_entity = await repo.get("apple", "en", "en")

    # Assertions
    assert word_entity is not None
    assert word_entity.word == "apple"
    assert word_entity.language == "en"

    # Check if related data is loaded correctly
    assert len(word_entity.definitions) == 1
    assert word_entity.definitions[0].definition == "A fruit"

    assert len(word_entity.synonyms) == 1
    assert word_entity.synonyms[0].synonym == "pome"

    assert len(word_entity.translations) == 1
    assert word_entity.translations[0].translation == "manzana"

    assert len(word_entity.examples) == 1
    assert word_entity.examples[0].example == "An apple a day keeps the doctor away."

    # Clean up - delete the test data
    await session.delete(test_definition)
    await session.delete(test_synonym)
    await session.delete(test_translation)
    await session.delete(test_example)
    await session.delete(test_word)
    await session.commit()


async def test_get_id_success(session: AsyncSession):
    # Setup test data
    test_word = WordModel(word="apple", language="en", word_id=1)
    session.add(test_word)
    await session.commit()

    # Instantiate the repository
    repo = WordPgRepo(_session_factory=lambda: session)

    # Test the get_id method
    word_id = await repo.get_id("apple", "en")

    assert word_id == 1

    # Clean up
    await session.delete(test_word)
    await session.commit()


async def test_get_id_not_found(session: AsyncSession):
    # Instantiate the repository
    repo = WordPgRepo(_session_factory=lambda: session)

    # Test the get_id method
    word_id = await repo.get_id("nonexistent", "en")

    # Assertions
    assert word_id is None


async def test_get_id_multiple_results(session: AsyncSession):
    # Setup test data
    test_word1 = WordModel(word="apple", language="en", word_id=1)
    test_word2 = WordModel(word="apple", language="en", word_id=2)
    session.add_all([test_word1, test_word2])
    await session.commit()

    # Instantiate the repository
    repo = WordPgRepo(_session_factory=lambda: session)

    # Test the get_id method and expect an exception
    with pytest.raises(UndefinedWordException):
        await repo.get_id("apple", "en")

    # Clean up
    await session.delete(test_word1)
    await session.delete(test_word2)
    await session.commit()
