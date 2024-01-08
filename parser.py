import asyncio
import aiohttp
import json

from logger import logger
from config import cfg
from client import Client


class Parser:
    def __init__(self):
        ...

    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        logger.info("Starting parser")

        async with aiohttp.ClientSession() as session:
            client = Client(session)
            self.dump(await client.get_strains())

    def dump(self, strains):
        with open(cfg.dump_name, "w") as f:
            json.dump({k: v.dict() for k, v in strains.items()}, f)
