from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.api.deps import WordRepo, get_word_repo
from app.api.v1.schemas import WordSchema

TAG = "word"
PREFIX = f"/{TAG}"

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{word_text}", response_model=WordSchema)
async def get_word(
    word_text: str,
    sl: str = "auto",
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
