from dataclasses import dataclass
from typing import Optional

from app.domain.entities import WordEntity
from app.repo.google.word import GoogleWordRepo
from app.repo.pg.word import WordPgRepo


@dataclass
class WordRepo:
    """Access to word entity."""

    pg_repo: "WordPgRepo"
    google_repo: "GoogleWordRepo"

    async def get(self, word: str, sl: str, tl: str) -> WordEntity:
        word_entity = await self.pg_repo.get(word, sl, tl)

        if word_entity is None:
            word_entity = await self.google_repo.get(word, sl, tl)

        if word_entity:
            await self.pg_repo.save(word_entity)

        return word_entity

    async def delete(self, word: str, sl: str) -> None:
        """Idempotent delete function.

        :raises UndefinedWordException: find multiple words by given filters.
        """

        id = await self.pg_repo.get_id(word, sl)

        if not id:
            return

        await self.pg_repo.delete(id)

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

        return await self.pg_repo.get_pages(
            page,
            page_size,
            word_filter,
            include_definitions,
            include_synonyms,
            include_translations,
            include_examples,
        )
