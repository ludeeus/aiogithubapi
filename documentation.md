## Example usage of AIOGitHubAPI

```python
import asyncio
from aiogithubapi import GitHub, GitHubDevice

CLIENT_ID = "XXXXX..."
TOKEN = "XXXXX..."


async def with_device_flow():
    """Example usage of AIOGitHubAPI."""
    async with GitHubDevice(CLIENT_ID) as device_login:
        device = await device_login.async_register_device()
        print("Open https://github.com/login/device and enter:", device.user_code)
        activation = await device_login.async_device_activation()

    async with GitHub(activation.access_token) as github:
        repository = await github.get_repo("ludeeus/aiogithubapi")
        print("Repository description:", repository.full_name)
        print("Repository description:", repository.description)


async def with_token():
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("ludeeus/aiogithubapi")
        print("Repository description:", repository.full_name)
        print("Repository description:", repository.description)


asyncio.get_event_loop().run_until_complete(with_token())
```