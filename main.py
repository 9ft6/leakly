import asyncio
import aiohttp

from client import Client
from dataset import Strains


async def main():
    dataset = Strains()

    async with aiohttp.ClientSession() as session:
        client = Client(session, dataset)
        await client.update()

    # dataset.show()
    dataset.export()


if __name__ == '__main__':
    asyncio.run(main())
