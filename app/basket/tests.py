import http

import pytest

from users.auth.services import get_current_user_from_token


class TestGetBasketProducts:
    @pytest.mark.asyncio
    async def test_get_basket_products(self, client, test_db, user_token, basket_product_factory):
        user = await get_current_user_from_token(test_db, str(user_token))
        basket_products = await basket_product_factory.create_batch(user_id=user.id, size=3)

        resp = await client.get(
            url="/api/basket/",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()["basket_products"]) == len(basket_products)
        assert sorted([p.id for p in basket_products]) == sorted(
            [data["id"] for data in resp.json()["basket_products"]]
        )

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, basket_product_factory, user_factory):
        user = await user_factory()
        basket_products = await basket_product_factory.create_batch(user_id=user.id, size=3)

        resp = await client.get(
            url="/api/basket/",
        )
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED


class TestCreateBasketProduct:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, user_token, product_variant_factory):
        product_variant = await product_variant_factory()

        data = {
            "product_variant_id": product_variant.id,
            "count": 2,
        }

        resp = await client.post(
            url="/api/basket/add_product/",
            json=data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["product_variant_id"] == data["product_variant_id"]
        assert resp.json()["count"] == data["count"]

    @pytest.mark.asyncio
    async def test_negative_count(self, client, user_token, product_variant_factory):
        product_variant = await product_variant_factory()

        data = {
            "product_variant_id": product_variant.id,
            "count": -2,
        }

        resp = await client.post(
            url="/api/basket/add_product/",
            json=data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

        resp = await client.get(
            url="/api/basket/",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.json()["basket_price"] == 0
        assert len(resp.json()["basket_products"]) == 0

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, user_token, product_variant_factory):
        product_variant = await product_variant_factory()

        data = {
            "product_variant_id": product_variant.id,
            "count": 2,
        }

        resp = await client.post(
            url="/api/basket/add_product/",
            json=data,
        )
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(
            url="/api/basket/",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.json()["basket_price"] == 0
        assert len(resp.json()["basket_products"]) == 0


class TestUpdateBasketProduct:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, test_db, user_token, basket_product_factory):
        user = await get_current_user_from_token(test_db, str(user_token))
        basket_product = await basket_product_factory(user_id=user.id, count=1)

        data = {"count": 5}

        resp = await client.patch(
            url=f"/api/basket/update_product/{basket_product.id}",
            json=data,
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["count"] == data["count"]

    @pytest.mark.asyncio
    async def test_update_basket_product_of_another_user(
        self, client, user_token, basket_product_factory, user_factory
    ):
        user = await user_factory()
        basket_product = await basket_product_factory(user_id=user.id, count=1)

        data = {"count": 5}

        resp = await client.patch(
            url=f"/api/basket/update_product/{basket_product.id}",
            json=data,
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, user_token, test_db, basket_product_factory):
        user = await get_current_user_from_token(test_db, str(user_token))
        basket_product = await basket_product_factory(user_id=user.id, count=1)

        data = {"count": 5}

        resp = await client.patch(
            url=f"/api/basket/update_product/{basket_product.id}",
            json=data,
        )

        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(
            url=f"/api/basket/",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.json()["basket_products"][0]["count"] == basket_product.count


class TestDeleteBasketProduct:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, user_token, test_db, basket_product_factory):
        user = await get_current_user_from_token(test_db, str(user_token))
        basket_product = await basket_product_factory(user_id=user.id)

        resp = await client.delete(
            url=f"/api/basket/delete_product/{basket_product.id}", headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == http.HTTPStatus.OK

        resp = await client.get(
            url="/api/basket/",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert len(resp.json()["basket_products"]) == 0

    @pytest.mark.asyncio
    async def test_delete_basket_product_of_another_user(
        self, client, user_token, basket_product_factory, user_factory
    ):
        user = await user_factory()
        basket_product = await basket_product_factory(user_id=user.id)

        resp = await client.delete(
            url=f"/api/basket/delete_product/{basket_product.id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, user_token, test_db, basket_product_factory):
        user = await get_current_user_from_token(test_db, str(user_token))
        basket_product = await basket_product_factory(user_id=user.id)

        resp = await client.delete(url=f"/api/basket/delete_product/{basket_product.id}")
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(
            url="/api/basket/",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert len(resp.json()["basket_products"]) == 1
