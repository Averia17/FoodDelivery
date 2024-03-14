import http

import pytest


class TestGetIngredients:
    @pytest.mark.asyncio
    async def test_get_ingredients(self, client, ingredient_factory):
        ingredients = await ingredient_factory.create_batch(3)

        resp = await client.get("api/ingredients/")
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == len(ingredients)
        assert sorted([p.id for p in ingredients]) == sorted([data["id"] for data in resp.json()])

    @pytest.mark.asyncio
    async def test_get_detailed_ingredient(self, client, ingredient_factory):
        ingredient = await ingredient_factory()

        resp = await client.get(f"api/ingredients/{ingredient.id}")
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["name"] == ingredient.name

    @pytest.mark.asyncio
    async def test_get_ingredient_witch_doesnt_exist(self, client):
        resp = await client.get(f"api/ingredients/1")
        assert resp.status_code == http.HTTPStatus.NOT_FOUND


class TestCreateIngredients:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, manager_token):
        data = {"name": "some_name"}

        resp = await client.post(
            url="/api/ingredients/",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["name"] == data["name"]

    @pytest.mark.asyncio
    async def test_unauthorized(self, client):
        data = {"name": "some_name"}

        resp = await client.post(
            url="/api/ingredients/",
            json=data,
        )
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get("api/ingredients/")
        assert len(resp.json()) == 0


class TestUpdateIngredients:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, ingredient_factory, manager_token):
        ingredient = await ingredient_factory()
        data = {"name": "ingredient1"}

        resp = await client.patch(
            url=f"/api/ingredients/{ingredient.id}",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )

        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["name"] == data["name"]

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, ingredient_factory):
        ingredient = await ingredient_factory()
        data = {"name": "ingredient1"}

        resp = await client.patch(
            url=f"/api/ingredients/{ingredient.id}",
            json=data,
        )
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(f"api/ingredients/{ingredient.id}")
        assert resp.json()["name"] == ingredient.name


class TestDeleteIngredients:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, ingredient_factory, manager_token):
        ingredient = await ingredient_factory()

        resp = await client.delete(
            url=f"/api/ingredients/{ingredient.id}", headers={"Authorization": f"Bearer {manager_token}"}
        )
        assert resp.status_code == http.HTTPStatus.OK

        resp = await client.get(f"api/ingredients/{ingredient.id}")
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, ingredient_factory):
        ingredient = await ingredient_factory()

        resp = await client.patch(
            url=f"/api/ingredients/{ingredient.id}",
        )
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(f"api/ingredients/{ingredient.id}")
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["name"] == ingredient.name
