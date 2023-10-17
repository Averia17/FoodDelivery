import pytest
from httpx import AsyncClient

from products.tests.conftest import app


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("/", {"app": "working"}),
        ("/products/", []),
    ],
    ids=["test1", "test2"],
)
async def test_get_product(test_input, expected):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(test_input)
    assert response.json() == expected
