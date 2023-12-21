from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import contains_eager, joinedload
from sqlalchemy.orm.exc import MultipleResultsFound

from app.domain.entities import WordEntity
from app.models import Definition as DefinitionModel
from app.models import Example as ExampleModel
from app.models import Synonym as SynonymModel
from app.models import Translation as TranslationModel
from app.models import Word as WordModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UndefinedWordException(BaseException):
    """Cannot define word by given parameters."""

    pass


@dataclass
class WordPgRepo:
    """Access to word entity inside database."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get(self, word: str, sl: str, tl: str) -> WordEntity:
        """Retrieves a WordEntity from the database based on the provided word, source
        language (sl), and target language (tl). The method performs an inner join with
        the DefinitionModel to ensure the existence of a definition for the word in the target
        language, which implies the presence of a translation.
        Synonyms, translations, and examples are joined using left joins, allowing
        their absence.
        """
        async with self._session_factory() as session:

            # do an inner join with the table defenition with the assumption,
            # that the absence of a defenition means the absence of a translation
            # left join for other cases
            query = (
                select(WordModel)
                .join(
                    DefinitionModel,
                    (WordModel.word_id == DefinitionModel.word_id)
                    & (DefinitionModel.language == tl),
                )
                .options(contains_eager(WordModel.definitions))
                .join(
                    SynonymModel,
                    (WordModel.word_id == SynonymModel.word_id)
                    & (SynonymModel.language == tl),
                    isouter=True,
                )
                .options(contains_eager(WordModel.synonyms))
                .join(
                    TranslationModel,
                    (WordModel.word_id == TranslationModel.word_id)
                    & (TranslationModel.language == tl),
                    isouter=True,
                )
                .options(contains_eager(WordModel.translations))
                .join(
                    ExampleModel,
                    (WordModel.word_id == ExampleModel.word_id)
                    & (ExampleModel.language == tl),
                    isouter=True,
                )
                .options(contains_eager(WordModel.examples))
                .where(WordModel.word == word)
            )

            if sl != "auto":
                query = query.where(WordModel.language == sl)

            result = await session.execute(query)
            word = result.scalars().first()

            return WordEntity.model_validate(word) if word else None

    async def get_id(self, word: str, sl: str) -> int:
        """Retrieves the unique identifier (ID) of a word from the database based on
        the specified word and source language (sl).
        This method is designed to fetch the ID of a word where the word and
        its language match the given parameters.
        """
        async with self._session_factory() as session:
            query = select(WordModel.word_id).where(WordModel.word == word)

            if sl != "auto":
                query = query.where(WordModel.language == sl)

            result = await session.execute(query)

            try:
                id = result.one_or_none()
            except MultipleResultsFound:
                raise UndefinedWordException(
                    "Cannot define word by given parameters. Multiple words were found."
                ) from MultipleResultsFound
            return id[0] if id else None

    async def delete(self, word_id: int) -> None:
        """Deletes a word and its related data (definitions, synonyms, translations,
            and examples) from the database based on the provided word ID.

        This method executes multiple delete operations to remove all associated data
        from the related tables (ExampleModel, TranslationModel, SynonymModel, DefinitionModel)
        before finally deleting the word from the WordModel. The deletions are not done via
        cascade delete in the database, but rather through individual delete statements
        in this method."""

        async with self._session_factory() as session:
            # This one should be improved by delete cascade.
            # Due to problems with cascade declaration here is a fast approach
            await session.execute(
                delete(ExampleModel).where(WordModel.word_id == word_id)
            )
            await session.execute(
                delete(TranslationModel).where(WordModel.word_id == word_id)
            )
            await session.execute(
                delete(SynonymModel).where(WordModel.word_id == word_id)
            )
            await session.execute(
                delete(DefinitionModel).where(WordModel.word_id == word_id)
            )
            await session.execute(delete(WordModel).where(WordModel.word_id == word_id))

    async def get_pages(
        self,
        page: int,
        page_size: int = 10,
        word_filter: Optional[str] = None,
        include_definitions: Optional[bool] = False,
        include_synonyms: Optional[bool] = False,
        include_translations: Optional[bool] = False,
        include_examples: Optional[bool] = False,
    ) -> list["WordModel"]:
        """Retrieves a paginated list of words from the database,
        with optional filters and related data.

        This method supports pagination, filtering by a word substring, and optional inclusion of
        related data such as definitions, synonyms, translations, and examples. The related data
        is included based on the respective boolean flags.
        """

        async with self._session_factory() as session:
            stmt = select(WordModel).order_by(WordModel.word)

            if word_filter:
                stmt = stmt.where(WordModel.word.ilike(f"%{word_filter}%"))

            if include_definitions:
                stmt = stmt.options(joinedload(WordModel.definitions))
            if include_synonyms:
                stmt = stmt.options(joinedload(WordModel.synonyms))
            if include_translations:
                stmt = stmt.options(joinedload(WordModel.translations))
            if include_examples:
                stmt = stmt.options(joinedload(WordModel.examples))

            stmt = stmt.offset((page - 1) * page_size).limit(page_size)

            result = await session.execute(stmt)

            return result.unique().scalars().all()
            # return [WordEntity.model_validate(word) for word in words]

    async def save(self, word: WordEntity):
        """Saves a WordEntity instance into the database.

        If the word already exists in the database, this method will skip creating a new entry.
        If the word does not exist, it creates a new WordModel instance and
        saves it to the database.
        """

        async with self._session_factory() as session:
            # Check if the word already exists
            stmt = select(WordModel).where(
                WordModel.word == word.word, WordModel.language == word.language
            )
            result = await session.execute(stmt)
            word_record = result.scalar_one_or_none()

            if word_record is None:
                # Create a new WordModel instance
                word_record = WordModel(word=word.word, language=word.language)
                session.add(word_record)
                await session.commit()

        async with self._session_factory() as session:

            # Insert/Ignore Definitions
            for definition in word.definitions:
                insert_stmt = insert(DefinitionModel).values(
                    definition=definition.definition,
                    word_id=word_record.word_id,
                    language=definition.language,
                )
                await session.execute(insert_stmt.on_conflict_do_nothing())

            # Insert/Ignore Synonyms
            for synonym in word.synonyms:
                insert_stmt = insert(SynonymModel).values(
                    synonym=synonym.synonym,
                    word_id=word_record.word_id,
                    language=synonym.language,
                )
                await session.execute(insert_stmt.on_conflict_do_nothing())

            # Insert/Ignore Translations
            for translation in word.translations:
                insert_stmt = insert(TranslationModel).values(
                    translation=translation.translation,
                    word_id=word_record.word_id,
                    language=translation.language,
                )
                await session.execute(insert_stmt.on_conflict_do_nothing())

            # Insert/Ignore Examples
            for example in word.examples:
                insert_stmt = insert(ExampleModel).values(
                    example=example.example,
                    word_id=word_record.word_id,
                    language=example.language,
                )
                await session.execute(insert_stmt.on_conflict_do_nothing())

            await session.commit()
