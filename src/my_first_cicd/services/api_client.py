import asyncio

import httpx
from httpx import AsyncClient, Response
from loguru import logger

from src.my_first_cicd.services.http_client import SEM, HTTPClient

URLS: list[str] = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/3",
    "https://www.python-httpx.org/advanced/transports/#custom-transports",
    "https://docs-python.ru/packages/modul-httpx-python/asinhronnyi-klient-httpx-asynccliet/"
]

async def send_request(
       client: AsyncClient,
       method: str,
       url: str,
       semaphore: int,
       max_retries: int = 3,
) -> Response | dict[str, str | int] | None:
    attempt: int = 0
    async with semaphore:
        for attempt in range(1, max_retries + 1):
            try:
                response = await client.request(method, url)
                response.raise_for_status()
                return response
            except (httpx.TimeoutException, httpx.HTTPStatusError, httpx.NetworkError):
                if attempt == max_retries:
                    return {"url": url, "status": response.status_code}
                logger.debug(f"Возникла ошибка при отправке запроса на {url}. Делаем повторный запрос..")
                await asyncio.sleep(2 * attempt)
        return None


async def main() -> None:
    async with HTTPClient() as client:
        global URLS
        tasks = (send_request(client, 'GET', url, SEM) for url in URLS)
        results: list[BaseException] = await asyncio.gather(*tasks, return_exceptions=True)
        good_results: list[BaseException] = []
        for result in results:
            if isinstance(result, Exception):
                logger.warning(f"При обращении к внешнему API возникло исключение: {result}")
            else:
                good_results.append(result)

        for url, result in zip(URLS, good_results):
            logger.info(f"URL {url}, response: {result}")


if __name__ == "__main__":
    asyncio.run(main())

