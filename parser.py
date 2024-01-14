import asyncio
import aiohttp

from logger import logger
from client import Client


class Parser:
    def __init__(self, dataset):
        self.dataset = dataset

    def run(self):
        return asyncio.run(self._run())

    async def _run(self):
        logger.info("Starting strains parser")
        async with aiohttp.ClientSession() as session:
            return await Client(session).get_strains(self.dataset)
