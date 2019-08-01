"""Example usage of AIOGitHub."""
import asyncio
import aiohttp
from aiogithubapi import AIOGitHub

TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


async def example():
    """Example usage of pyhaversion."""
    async with aiohttp.ClientSession() as session:
        aiogithub = AIOGitHub(TOKEN, session)
        repository = await aiogithub.get_repo("ludeeus/aiogithubapi")

        print("Ratelimit remaining:", aiogithub.ratelimits.remaining)
        print("Ratelimit reset UTC:", aiogithub.ratelimits.reset_utc)
        print("Repository description:", repository.description)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(example())
