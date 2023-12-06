from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import WordPgRepo, get_word_repo
from app.api.v1.mapper import map_word
from app.api.v1.schemas import WordSchema

TAG = "word"
PREFIX = f"/{TAG}"

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{word_text}", response_model=WordSchema)
async def get_word_details(
    word_text: str,
    sl: str = "auto",
    tl: str = Query(..., description="Target language"),
    repo: "WordPgRepo" = Depends(get_word_repo),
):

    word = await repo.get(word_text, sl, tl)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    return map_word(word)
