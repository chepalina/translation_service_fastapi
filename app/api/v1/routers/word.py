from fastapi import APIRouter

TAG = "example"
PREFIX = f"/{TAG}"

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", summary="Test GET query.")
async def example() -> None:
    return None
