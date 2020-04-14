# AIOGitHubAPI
[![codecov](https://codecov.io/gh/ludeeus/aiogithubapi/branch/master/graph/badge.svg)](https://codecov.io/gh/ludeeus/aiogithubapi)

_Asynchronous Python client for the GitHub API_

This is not a full client for the API (Have you seen it, it's huge), and will probably never be.
Things are added when needed.

## Install

```bash
python3 -m pip install -U aiogithubapi
```

## Example

```python
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
```