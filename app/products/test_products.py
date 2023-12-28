import http

import pytest


@pytest.mark.asyncio
async def test_get_products(client, product_factory):
    products = await product_factory.create_batch(3)

    resp = await client.get('api/products/')
    assert resp.status_code == http.HTTPStatus.OK
    assert len(resp.json()) == len(products)
    assert sorted([p.id for p in products]) == sorted([data['id'] for data in resp.json()])

    resp = await client.get(f'api/products/{products[0].id}')
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['name'] == products[0].name


@pytest.mark.asyncio
async def test_create_product(client, category_factory, token_manager):
    category = await category_factory()
    data = {'name': 'product1', 'price': 2.0, 'category_id': f'{category.id}'}

    resp = await client.post(url="/api/products/", json=data)
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

    resp = await client.post(
        url="/api/products/",
        json=data,
        headers={"Authorization": f"Bearer {token_manager}"}
    )
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['name'] == data['name']


@pytest.mark.asyncio
async def test_update_product(client, product_factory, token_manager):
    product = await product_factory()
    data = {'name': 'product1'}

    resp = await client.patch(url=f'/api/products/{product.id}', json=data)
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

    resp = await client.patch(
        url=f'/api/products/{product.id}',
        json=data,
        headers={"Authorization": f"Bearer {token_manager}"}
    )

    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['name'] == data['name']


@pytest.mark.asyncio
async def test_delete_product(client, product_factory, token_manager):
    product = await product_factory()

    resp = await client.delete(url=f'/api/products/{product.id}')
    assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

    resp = await client.delete(
        url=f'/api/products/{product.id}',
        headers={"Authorization": f"Bearer {token_manager}"}
    )
    assert resp.status_code == http.HTTPStatus.OK


