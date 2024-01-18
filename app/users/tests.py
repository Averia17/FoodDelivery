import http

import pytest

from users.models import User


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_valid_data(self, client):
        data = {"email": "test@test.com", "password": "testpassword", "phone_number": "+375291234567"}

        resp = await client.post(url="/api/users/", json=data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()["email"] == data["email"]
        assert resp.json()["phone_number"] == data["phone_number"]

    @pytest.mark.asyncio
    async def test_invalid_phone_number(self, client, test_db):
        data = {"email": "test@test.com", "password": "testpassword", "phone_number": "+000112224567"}

        resp = await client.post(url="/api/users/", json=data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert not await User.get_by_email(test_db, data["email"])

    @pytest.mark.asyncio
    async def test_without_email(self, client):
        data = {"password": "testpassword", "phone_number": "+375291234567"}

        resp = await client.post(url="/api/users/", json=data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert resp.json()["errors"]["email"][0] == "Field required"
