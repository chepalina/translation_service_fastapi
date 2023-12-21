from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.main import app
from app.api.deps import get_word_repo  # Import your FastAPI app and dependency
from app.api.v1.schemas import WordSchema, DefinitionSchema, SynonymSchema, TranslationSchema, ExampleSchema
import pytest_asyncio

from fastapi.testclient import TestClient
import pytest

class MockRepo:
    async def get(self, word_text, sl, tl):
        return WordSchema(
            word=word_text,
            language=sl,
            definitions=[DefinitionSchema(definition="A greeting")],
            synonyms=[SynonymSchema(synonym="hello")],
            translations=[TranslationSchema(translation="hola")],
            examples=[ExampleSchema(example="Hello, how are you?")]
        )
from collections.abc import AsyncGenerator
from httpx import AsyncClient

import pytest
import httpx
from http import HTTPStatus
from unittest.mock import AsyncMock

@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_word_success(client):
    # Mock the WordRepo dependency
    get_word_repo_mock =  MockRepo()
    client = TestClient(app)

    app.dependency_overrides[get_word_repo] = get_word_repo_mock

    # Test successful retrieval
    response = client.get("/api/v1/words/example?sl=en&tl=es")
    assert response.json() == ""
    assert response.status_code == 200
    assert response.json() == {"word": "example", "meaning": "A sample word"}
#
# @pytest.mark.asyncio
# async def test_get_word_not_found(async_client):
#     # Mock the WordRepo dependency to return None
#     get_word_repo_mock = AsyncMock()
#     get_word_repo_mock.get.return_value = None
#
#     # Test word not found scenario
#     response = await async_client.get("/nonexistent?sl=en&tl=es", dependencies={"get_word_repo": get_word_repo_mock})
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {"detail": "Word not found"}

# Additional async tests can be added similarly
