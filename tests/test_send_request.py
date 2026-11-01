import httpx
import pytest
import respx

from src.my_first_cicd.services.http_client import SEM
from src.my_first_cicd.services.api_client import send_request


pytestmark = pytest.mark.asyncio


# 1. Успешный запрос с первого раза
@respx.mock
async def test_success(client):
    url = "https://example.com/ok"
    respx.get(url).mock(return_value=httpx.Response(200, json={"ok": True}))

    response = await send_request(client, "GET", url, SEM)

    assert response.status_code == 200
    assert response.json() == {"ok": True}


# 2. Ретраи: 500 → 500 → 200, успех на 3-й попытке
@respx.mock
async def test_retries_then_success(client):
    url = "https://example.com/retry"
    route = respx.get(url).mock(
        side_effect=[
            httpx.Response(500),
            httpx.Response(500),
            httpx.Response(200),
        ]
    )

    response = await send_request(client, "GET", url, SEM, max_retries=3)

    assert route.call_count == 3
    assert response.status_code == 200


# 3. Все попытки упали → возвращается dict с url и status
@respx.mock
async def test_exhausted_returns_dict(client):
    url = "https://example.com/fail"
    respx.get(url).mock(return_value=httpx.Response(503))

    result = await send_request(client, "GET", url, SEM, max_retries=2)

    assert isinstance(result, dict)
    assert result["url"] == url
    assert result["status"] == 503