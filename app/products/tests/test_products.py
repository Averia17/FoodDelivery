import http

import pytest


@pytest.mark.asyncio
async def test_get_products(client, product_factory):
    products = await product_factory.create_batch(3)

    resp = await client.get("api/products/")
    assert resp.status_code == http.HTTPStatus.OK
    assert len(resp.json()) == len(products)
    assert sorted([p.id for p in products]) == sorted([data["id"] for data in resp.json()])
