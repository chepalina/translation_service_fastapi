from http import HTTPStatus
from typing import Optional

import strawberry
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from strawberry.fastapi import GraphQLRouter

from app.api.deps import WordRepo, get_strawberry_context, get_word_repo
from app.api.v1.schemas import WordSchema
from app.api.v1.types import WordType

TAG = "word"
PREFIX = f"/{TAG}"

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{word_text}", response_model=WordSchema)
async def get_word(
    word_text: str,
    sl: str = Query(..., description="Source language"),
    tl: str = Query(..., description="Target language"),
    repo: "WordRepo" = Depends(get_word_repo),
):

    word = await repo.get(word_text, sl, tl)
    if not word:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Word not found")

    return word


@router.delete("/word/{word_text}", status_code=HTTPStatus.NO_CONTENT)
async def delete_word(
    word_text: str = Path(..., description="Word to delete"),
    sl: str = "auto",
    repo: "WordRepo" = Depends(get_word_repo),
):

    await repo.delete(word_text, sl)

    return HTTPStatus.NO_CONTENT


@strawberry.type
class WordQuery:
    @strawberry.field
    async def words(
        self,
        info,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        word_filter: Optional[str] = None,
        include_definitions: Optional[bool] = False,
        include_synonyms: Optional[bool] = False,
        include_translations: Optional[bool] = False,
        include_examples: Optional[bool] = False,
    ) -> list[WordType]:
        word_repo = info.context["word_repo"]
        words = await word_repo.get_pages(
            page,
            page_size,
            word_filter,
            include_definitions,
            include_synonyms,
            include_translations,
            include_examples,
        )

        return [
            WordType(
                word=word.word,
                language=word.language,
                definitions=word.definitions if include_definitions else None,
                synonyms=word.synonyms if include_synonyms else None,
                translations=word.translations if include_translations else None,
                examples=word.examples if include_examples else None,
            )
            for word in words
        ]


schema = strawberry.Schema(WordQuery)

graphql_router = GraphQLRouter(schema, context_getter=get_strawberry_context)
