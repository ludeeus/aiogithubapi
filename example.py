"""Example usage of AIOGitHubAPI"""
import asyncio
from aiogithubapi import GitHub


async def example():
    """Example usage of AIOGitHubAPI."""
    async with GitHub() as github:
        repository = await github.get_repo("ludeeus/aiogithubapi")
        print("Repository description:", repository.full_name)
        print("Repository description:", repository.description)


asyncio.get_event_loop().run_until_complete(example())
