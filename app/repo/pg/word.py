from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from app.domain.entities import WordEntity
from app.models import Definition as DefinitionModel
from app.models import Example as ExampleModel
from app.models import Synonym as SynonymModel
from app.models import Translation as TranslationModel
from app.models import Word as WordModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


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


# from app.core.session import get_context
# from asyncio import run
# repo = WordPgRepo(_session_factory=get_context)
# w = run(repo.get("apple"))
#
# print(w)
