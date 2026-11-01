import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.my_first_cicd.services.http_client import HTTPClient


@pytest_asyncio.fixture
async def client():
    async with HTTPClient() as c:
        yield c