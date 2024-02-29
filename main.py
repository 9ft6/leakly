import asyncio
import aiohttp

from client import Client
from dataset import Strains
from config import cfg


async def main(update=None):
    dataset = Strains()

    if update or cfg.update_strains:
        async with aiohttp.ClientSession() as session:
            client = Client(session, dataset)
            await client.update()

    # dataset.show()
    # dataset.export()
    # dataset.show(_filter=None)


if __name__ == '__main__':
    asyncio.run(main())
