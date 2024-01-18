import http

import pytest

from users.auth.services import get_password_hash


@pytest.mark.asyncio
async def test_login_for_access_token(client, user_factory):
    password = "some_password"
    hash_password = get_password_hash(password)
    user = await user_factory(password=hash_password)
    data = {"username": user.email, "password": password}

    resp = await client.post(url="/api/auth/token", data=data)
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()["access_token"]
    assert resp.json()["refresh_token"]
