from dataclasses import dataclass
from typing import Optional

from app.domain.entities import WordEntity
from app.repo.pg.word import WordPgRepo


@dataclass
class WordRepo:
    """Access to word entity."""

    pg_repo: "WordPgRepo"

    async def get(self, word: str, sl: str, tl: str) -> WordEntity:
        return await self.pg_repo.get(word, sl, tl)

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
    ) -> list["WordEntity"]:

        return await self.pg_repo.get_pages(
            page,
            page_size,
            word_filter,
            include_definitions,
            include_synonyms,
            include_translations,
            include_examples,
        )
