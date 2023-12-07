from dataclasses import dataclass

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
