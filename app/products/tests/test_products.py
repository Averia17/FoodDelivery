import pytest

from sqlalchemy import true, null


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("/", {"app": "working"}),
        (
            "/products/3/",
            {
                "id": 3,
                "name": "string2",
                "is_active": true,
                "description": null,
                "discount": 0,
                "price": 2.0,
                "category_id": 1,
            },
        ),
    ],
    ids=["test1", "test2"],
)
def test_get_product(test_input, expected, client):
    r = client.get(test_input)
    assert r.json() == expected
