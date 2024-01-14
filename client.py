import asyncio

import aiohttp

from models import Strain, Comment
from config import cfg
from logger import logger


class Client:
    session: aiohttp.ClientSession

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_comments_by_strain(self, strain: Strain):
        url, params = self.get_comment_url(strain)
        response, status = await self._make_request(url, params=params)
        total = response["metadata"]["totalCount"]
        tasks = [self.get_comments_page(strain, s) for s in range(0, total, cfg.comments_one_time)]
        comments = []
        for result in await asyncio.gather(*tasks):
            comments.extend(result)

        strain.comments = comments

    async def get_comments_page(self, strain: Strain, skip: int = 0) -> list[Comment]:
        url, params = self.get_comment_url(strain, skip=skip)
        response, status = await self._make_request(url, params=params)
        return [Comment(**c) for c in response["data"]] if response else []

    async def get_strains(self, dataset):
        url, params = self.get_strain_url()
        response, status = await self._make_request(url, params=params)
        total = response["metadata"]["totalCount"]
        step = cfg.pages_one_time * cfg.items_per_page
        for n in range(0, total, step):
            tasks = [(i + 1) * cfg.items_per_page + n for i in range(cfg.pages_one_time)]
            tasks = [self.get_strain_page(s) for s in tasks]
            result = await asyncio.gather(*tasks)
            [dataset.put_strains(r) for r in result]

    async def get_strain_page(self, skip: int = 0) -> list:
        url, params = self.get_strain_url(skip=skip)
        response, status = await self._make_request(url, params=params)
        strains = [Strain(**s) for s in response["hits"]["strain"]]
        await asyncio.gather(*[self.get_comments_by_strain(s) for s in strains])
        return strains

    async def _make_request(self, url, method="GET", attempts=cfg.request_attempts, **kwargs):
        while attempts:
            try:
                async with self.session.request(method, url, **kwargs) as response:
                    # logger.debug(f"{url}: {response.status=}")
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
                        logger.error(f"Can not decode body JSON: {e}")
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
                ValueError,
            ) as error:
                attempts -= 1
                logger.warning(f"{url}: Got an error {error} during GET request")
                if not attempts:
                    break

                return await self._make_request(method, url, attempts=attempts, **kwargs)

        logger.error(f"{url}: Exceeded the number of attempts to perform {method.upper()} request")
        return None, None

    def get_strain_url(self, skip: int = 0, take: int = cfg.items_per_page):
        url = f"{cfg.host}{cfg.strain_url}"
        params = {
            "enableNewFilters": "true",
            "skip": skip,
            "strain_playlist": "",
            "take": take,
            "sort[0][strain_name]": "asc"
        }
        return url, params

    def get_comment_url(self, strain: Strain, skip: int = 0, take: int = cfg.items_per_page):
        url = f"{cfg.host}{cfg.comment_url}/{strain.slug}/reviews"
        params = {
            "skip": skip,
            "take": take,
            "sort[0][upvotes_count]": "desc"
        }
        return url, params
