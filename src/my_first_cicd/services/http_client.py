from typing import AsyncGenerator
import asyncio

import httpx
from httpx import Timeout, AsyncClient, Limits, AsyncHTTPTransport

SEM = asyncio.Semaphore(3)

class HTTPClient:
    def __init__(
           self,
           connect: float=5.0,
           read: float=10.0,
           write: float=5.0,
           pool: float=2.0,
           max_connections: int=100,
           max_keepalive_connections: int=20,
           keepalive_expiry: float=30.0,
           retries: int=3
    ) -> None:
        self._connect = connect
        self._read = read
        self._write = write
        self._pool = pool
        self._max_connections = max_connections
        self._max_keepalive_connections = max_keepalive_connections
        self._keepalive_expiry = keepalive_expiry
        self._retries = retries
        self._timeout = Timeout(
            connect=self._connect,
            read=self._read,
            write=self._write,
            pool=self._pool
        )
        self._limits = Limits(
            max_connections=self._max_connections,
            max_keepalive_connections=self._max_keepalive_connections,
            keepalive_expiry=self._keepalive_expiry
        )
        self._transport = AsyncHTTPTransport(retries=self._retries)
        self._client: AsyncClient | None = None

    async def __aenter__(self) -> AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url="https://api.example.com/v1",
                timeout=self._timeout,
                limits=self._limits,
                transport=self._transport,
                headers={
                    "User-Agent": "my-service/1.0",
                    "Accept": "application/json"
                },
                trust_env=False
            )
            print("The HTTP Client is created!")
        return self._client

    async def __aexit__(self, *args: str) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
            print("The http client is closed.")

