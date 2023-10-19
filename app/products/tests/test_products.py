import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("/", {"app": "working"}),
        ("api/products/", []),
    ],
    ids=["test1", "test2"],
)
async def test_get_product(test_input, expected):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(test_input)
    assert response.json() == expected


@pytest.mark.anyio
async def test_create_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("api/categories/", json={"name": "string"})
    assert response.json() == {"id": 1, "is_active": True, "name": "string"}


@pytest.mark.anyio
async def test_get_category():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("api/categories/")
    assert response.json() == [{"id": 1, "is_active": True, "name": "string"}]
