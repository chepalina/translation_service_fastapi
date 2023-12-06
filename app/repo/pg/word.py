from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING
from app.models import Word as WordModel
from app.domain.entities import WordEntity
from sqlalchemy import select
from sqlalchemy.orm import joinedload

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class WordPgRepo:
    """Access to word entity inside database."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get(self, word: str) -> WordEntity:
        """Get word entity from database.

        For now just take all known relations.
        TODO: Need to be filtered by language.
        """
        async with self._session_factory() as session:

            query = (
                select(WordModel)
                .options(joinedload(WordModel.definitions))
                .options(joinedload(WordModel.synonyms))
                .options(joinedload(WordModel.translations))
                .options(joinedload(WordModel.examples))
                .where(WordModel.word == word)
            )

            result = await session.execute(query)
            word = result.scalars().first()

            return WordEntity.model_validate(word)


# from app.core.session import get_context
# from asyncio import run
# repo = WordPgRepo(_session_factory=get_context)
# w = run(repo.get("apple"))
#
# print(w)
