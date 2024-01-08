import asyncio

import aiohttp

from models import Strain
from config import cfg
from logger import logger


class Client:
    session: aiohttp.ClientSession

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_strains(self):
        strains = {}
        response, status = await self._make_request(self.get_url(skip=len(strains)))
        total = response["metadata"]["totalCount"]
        step = cfg.pages_one_time * cfg.items_per_page
        for n in range(0, total, step):
            tasks = [(i + 1) * cfg.items_per_page + n for i in range(cfg.pages_one_time)]
            tasks = [self.get_page(s) for s in tasks]
            for result in await asyncio.gather(*tasks):
                strains.update(result)

        return strains

    async def get_page(self, skip: int = 0) -> dict:
        response, status = await self._make_request(self.get_url(skip=skip))
        strains = [Strain(**s) for s in response["hits"]["strain"]]
        return {s.id: s for s in strains}

    async def _make_request(self, url, method="GET", attempts=cfg.request_attempts, **kwargs):
        while attempts:
            try:
                async with self.session.request(method, url, **kwargs) as response:
                    if "/token" in url:
                        kwargs["headers"] = {"Content-Type": "application/json"}

                    logger.debug(f"{url}: {response.status=}")
                    if response.status >= 300:
                        logger.warning(f"{url}: got a {response.status} response code")
                        attempts -= 1
                        return await self._make_request(
                            method,
                            url,
                            attempts=attempts,
                            **kwargs,
                        )

                    try:
                        result = await response.json()
                    except Exception as e:
                        # logger.error(f"Can not decode body JSON: {e}")
                        result = await response.read()

                    # logger.debug(f"{url}: RESPONSE BODY: {result}")
                    return result, response.status
            except aiohttp.InvalidURL as error:
                logger.error(f"{url}: Invalid url: {error}")
                return None, None
            except aiohttp.ClientPayloadError as error:
                logger.error(f"{url}: Malformed payload: {error}")
                return None, None
            except (
                aiohttp.ClientConnectorError,
                aiohttp.ClientResponseError,
                aiohttp.ServerDisconnectedError,
                asyncio.TimeoutError,
            ) as error:
                attempts -= 1
                logger.warning(f"{url}: Got an error {error} during GET request")
                if not attempts:
                    break

                return await self._make_request(method, url, attempts=attempts, **kwargs)

        logger.error(f"{url}: Exceeded the number of attempts to perform {method.upper()} request")
        return None, None

    def get_url(self, skip: int = 0, take: int = cfg.items_per_page):
        return (f"{cfg.host}{cfg.api}?enableNewFilters=true&skip={skip}"
                f"&strain_playlist=&take={take}&sort[0][strain_name]=asc")
