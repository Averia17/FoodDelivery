import http

import pytest


@pytest.mark.asyncio
async def test_get_categories(client, category_factory):
    categories = await category_factory.create_batch(3)

    resp = await client.get('api/categories/')
    assert resp.status_code == http.HTTPStatus.OK
    assert len(resp.json()) == len(categories)
    assert sorted([p.id for p in categories]) == sorted([data['id'] for data in resp.json()])

    resp = await client.get(f'api/categories/{categories[0].id}')
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['name'] == categories[0].name


@pytest.mark.asyncio
async def test_create_category(client):
    data = {'name': 'category_1'}

    resp = await client.post(url="/api/categories/", json=data)
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['name'] == data['name']


@pytest.mark.asyncio
async def test_update_category(client, category_factory):
    category = await category_factory()
    data = {'name': 'category'}

    resp = await client.patch(url=f'/api/categories/{category.id}', json=data)
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['name'] == data['name']


@pytest.mark.asyncio
async def test_delete_category(client, category_factory):
    category = await category_factory()

    resp = await client.delete(url=f'/api/categories/{category.id}')
    assert resp.status_code == http.HTTPStatus.OK
