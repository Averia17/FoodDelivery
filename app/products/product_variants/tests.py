import http

import pytest


class TestGetProductVariants:
    @pytest.mark.asyncio
    async def test_get_product_variants(self, client, product_variant_factory):
        product_variants = await product_variant_factory.create_batch(3)

        resp = await client.get("api/product_variants/")
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == len(product_variants)
        assert sorted([p.id for p in product_variants]) == sorted([data["id"] for data in resp.json()])


class TestCreateProductVariant:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, manager_token, product_factory):
        product = await product_factory()

        data = {
            "product_id": product.id,
            "price": 2599,
            "discount": 25,
            "weight": 500,
        }

        resp = await client.post(
            url="/api/product_variants/",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["product_id"] == data["product_id"]
        assert resp.json()["price"] == data["price"]
        assert resp.json()["weight"] == data["weight"]

    @pytest.mark.asyncio
    async def test_negative_discount(self, client, manager_token, product_factory):
        product = await product_factory()

        data = {
            "product_id": product.id,
            "price": 2599,
            "discount": -1,
            "weight": 500,
        }
        resp = await client.post(
            url="/api/product_variants/",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

        resp = await client.get("api/product_variants/")
        assert len(resp.json()) == 0

    @pytest.mark.asyncio
    async def test_too_big_discount(self, client, manager_token, product_factory):
        product = await product_factory()

        data = {
            "product_id": product.id,
            "price": 2599,
            "discount": 100,
            "weight": 500,
        }

        resp = await client.post(
            url="/api/product_variants/",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

        resp = await client.get("api/product_variants/")
        assert len(resp.json()) == 0

    @pytest.mark.asyncio
    async def test_negative_price(self, client, manager_token, product_factory):
        product = await product_factory()

        data = {
            "product_id": product.id,
            "price": -5,
            "discount": 0,
            "weight": 500,
        }
        resp = await client.post(
            url="/api/product_variants/",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

        resp = await client.get("api/product_variants/")
        assert len(resp.json()) == 0

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, product_factory):
        product = await product_factory()

        data = {
            "product_id": product.id,
            "price": 2599,
            "weight": 500,
        }

        resp = await client.post(
            url="/api/product_variants/",
            json=data,
        )
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get("api/product_variants/")
        assert len(resp.json()) == 0


class TestUpdateProductVariant:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, product_variant_factory, manager_token):
        product_variant = await product_variant_factory()
        data = {"weight": 1000}

        resp = await client.patch(
            url=f"/api/product_variants/{product_variant.id}",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )

        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["weight"] == data["weight"]

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, product_variant_factory):
        product_variant = await product_variant_factory()
        data = {"weight": 1000}

        resp = await client.patch(
            url=f"/api/product_variants/{product_variant.id}",
            json=data,
        )
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(f"api/product_variants/")
        assert resp.json()[0]["weight"] == product_variant.weight


class TestDeleteProductVariant:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, product_variant_factory, manager_token):
        product_variant = await product_variant_factory()

        resp = await client.delete(
            url=f"/api/product_variants/{product_variant.id}", headers={"Authorization": f"Bearer {manager_token}"}
        )
        assert resp.status_code == http.HTTPStatus.OK

        resp = await client.get(f"api/product_variants/")
        assert len(resp.json()) == 0

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, product_variant_factory):
        product_variant = await product_variant_factory()

        resp = await client.patch(
            url=f"/api/product_variants/{product_variant.id}",
        )
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(f"api/product_variants/")
        assert len(resp.json()) == 1
        assert resp.json()[0]["weight"] == product_variant.weight
