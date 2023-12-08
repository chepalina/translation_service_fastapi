from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from sqlalchemy import delete, select
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
        """Get word entity from database."""
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
        """Get word entity from database."""

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
    ) -> list["WordEntity"]:

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
            words = result.unique().scalars().all()

            return [WordEntity.model_validate(word) for word in words]


# from app.core.session import get_context
# from asyncio import run
# repo = WordPgRepo(_session_factory=get_context)
# w = run(repo.get("apple"))
#
# print(w)
