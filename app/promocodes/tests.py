import datetime
import http

import pytest


class TestGetPromoCodes:
    @pytest.mark.asyncio
    async def test_get_promo_codes(self, client, manager_token, promo_code_factory):
        promo_codes = await promo_code_factory.create_batch(3)

        resp = await client.get(
            url="api/promo_codes/",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == len(promo_codes)
        assert sorted([p.id for p in promo_codes]) == sorted([data["id"] for data in resp.json()])

    @pytest.mark.asyncio
    async def test_get_detailed_promo_code(self, client, manager_token, promo_code_factory):
        promo_code = await promo_code_factory()

        resp = await client.get(
            url=f"api/promo_codes/{promo_code.id}",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["id"] == promo_code.id

    @pytest.mark.asyncio
    async def test_get_promo_code_which_doesnt_exist(self, client, manager_token):
        resp = await client.get(
            url=f"api/promo_codes/promo",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.asyncio
    async def test_not_manager(self, client, user_token, promo_code_factory):
        promo_code = await promo_code_factory()

        resp = await client.get(
            url=f"api/promo_codes/{promo_code.id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == http.HTTPStatus.FORBIDDEN


class TestCreatePromoCodes:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, manager_token, product_variant_factory):
        product_variant_1 = await product_variant_factory()
        product_variant_2 = await product_variant_factory()

        valid_from = datetime.datetime.now(datetime.UTC)
        valid_until = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        data = {
            "id": "some_promo_cod",
            "valid_from": str(valid_from),
            "valid_until": str(valid_until),
            "product_variants": [
                product_variant_1.id,
                product_variant_2.id,
            ],
            "discount": 1,
        }

        resp = await client.post(
            url="/api/promo_codes/",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["id"] == data["id"]

    @pytest.mark.asyncio
    async def test_empty_product_variants(self, client, manager_token, product_variant_factory):
        valid_from = datetime.datetime.now(datetime.UTC)
        valid_until = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        data = {
            "id": "some_promo_cod",
            "valid_from": str(valid_from),
            "valid_until": str(valid_until),
            "product_variants": [],
            "discount": 1,
        }

        resp = await client.post(
            url="/api/promo_codes/",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK

        promo_code_id = resp.json()["id"]
        resp = await client.get(
            url=f"api/promo_codes/{promo_code_id}",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["product_variants"] == []

    @pytest.mark.asyncio
    async def test_valid_until_earlier_than_valid_from(self, client, manager_token):
        valid_from = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        valid_until = datetime.datetime.now(datetime.UTC)
        data = {
            "id": "some_promo_cod",
            "valid_from": str(valid_from),
            "valid_until": str(valid_until),
        }

        resp = await client.post(
            url="/api/promo_codes/",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

        resp = await client.get(
            url="api/promo_codes/",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert len(resp.json()) == 0

    @pytest.mark.asyncio
    async def test_unauthorised(self, client, manager_token):
        valid_from = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        valid_until = datetime.datetime.now(datetime.UTC)
        data = {
            "id": "some_promo_cod",
            "valid_from": str(valid_from),
            "valid_until": str(valid_until),
        }

        resp = await client.post(
            url="/api/promo_codes/",
            json=data,
        )
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(
            url="api/promo_codes/",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert len(resp.json()) == 0


class TestUpdatePromoCodes:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, promo_code_factory, manager_token):
        promo_code = await promo_code_factory()
        valid_from = datetime.datetime.now(datetime.UTC)
        valid_until = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        data = {
            "valid_from": str(valid_from),
            "valid_until": str(valid_until),
            "discount": 50,
            "description": "some_description",
        }

        resp = await client.patch(
            url=f"/api/promo_codes/{promo_code.id}",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )

        assert resp.status_code == http.HTTPStatus.OK
        assert datetime.datetime.fromisoformat(resp.json()["valid_from"]) == datetime.datetime.fromisoformat(
            data["valid_from"]
        )
        assert datetime.datetime.fromisoformat(resp.json()["valid_until"]) == datetime.datetime.fromisoformat(
            data["valid_until"]
        )
        assert resp.json()["discount"] == data["discount"]
        assert resp.json()["description"] == data["description"]

    @pytest.mark.asyncio
    async def test_without_dates(self, client, promo_code_factory, manager_token):
        promo_code = await promo_code_factory()
        data = {
            "discount": 50,
            "description": "some_description",
        }

        resp = await client.patch(
            url=f"/api/promo_codes/{promo_code.id}",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )

        assert resp.status_code == http.HTTPStatus.OK
        assert datetime.datetime.fromisoformat(resp.json()["valid_from"]) == promo_code.valid_from
        assert datetime.datetime.fromisoformat(resp.json()["valid_until"]) == promo_code.valid_until
        assert resp.json()["discount"] == data["discount"]
        assert resp.json()["description"] == data["description"]

    @pytest.mark.asyncio
    async def test_valid_until_earlier_than_valid_from(self, client, promo_code_factory, manager_token):
        promo_code = await promo_code_factory(discount=5)
        valid_from = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        valid_until = datetime.datetime.now(datetime.UTC)
        data = {
            "valid_from": str(valid_from),
            "valid_until": str(valid_until),
            "discount": 50,
            "description": "some_description",
        }

        resp = await client.patch(
            url=f"/api/promo_codes/{promo_code.id}",
            json=data,
            headers={"Authorization": f"Bearer {manager_token}"},
        )

        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

        resp = await client.get(
            url=f"api/promo_codes/{promo_code.id}",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["discount"] == promo_code.discount

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, promo_code_factory, manager_token):
        promo_code = await promo_code_factory(discount=5)
        valid_from = datetime.datetime.now(datetime.UTC)
        valid_until = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
        data = {
            "valid_from": str(valid_from),
            "valid_until": str(valid_until),
            "discount": 50,
            "description": "some_description",
        }

        resp = await client.patch(
            url=f"/api/promo_codes/{promo_code.id}",
            json=data,
        )

        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(
            url=f"api/promo_codes/{promo_code.id}",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["discount"] == promo_code.discount


class TestDeletePromoCodes:
    @pytest.mark.asyncio
    async def test_valid_data(self, client, promo_code_factory, manager_token):
        promo_code = await promo_code_factory()

        resp = await client.delete(
            url=f"api/promo_codes/{promo_code.id}", headers={"Authorization": f"Bearer {manager_token}"}
        )
        assert resp.status_code == http.HTTPStatus.OK

        resp = await client.get(
            url=f"api/promo_codes/{promo_code.id}",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.asyncio
    async def test_unauthorized(self, client, promo_code_factory, manager_token):
        promo_code = await promo_code_factory()

        resp = await client.delete(url=f"api/promo_codes/{promo_code.id}")
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

        resp = await client.get(
            url=f"api/promo_codes/{promo_code.id}",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == http.HTTPStatus.OK
