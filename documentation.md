Note: When importing from this module, use \`from aiogithubapi import\`
Anything not available directly in aiogithubapi (defined in \`\_\_init\_\_.py\`)
is considered internal use only, and they can be removed without warning.

## Example usage of aiogithubapi

```python
"""Example usage of aiogithubapi."""
import asyncio
from aiogithubapi import GitHubAPI, GitHubDeviceAPI

CLIENT_ID = ""
TOKEN = ""


async def with_device_flow():
    """Example usage of aiogithubapi with Device OAuth flow."""
    async with GitHubDeviceAPI(client_id=CLIENT_ID) as device_login:
        registration = await device_login.register()
        print(
            f"Open https://github.com/login/device and enter: {registration.data.user_code}"
        )
        activation = await device_login.activation(device_code=registration.data.device_code)

    async with GitHubAPI(token=activation.data.access_token, **{"client_name": "MyClient/1.2.3"}) as github:
        repository = await github.async_get_repository("ludeeus/aiogithubapi")
        print("Repository name:", repository.data.name)
        print("Repository description:", repository.data.description)


async def with_token():
    """Example usage of aiogithubapi with PAT."""
    async with GitHubAPI(token=TOKEN, **{"client_name": "MyClient/1.2.3"}) as github:
        repository = await github.async_get_repository("ludeeus/aiogithubapi")
        print("Repository name:", repository.data.name)
        print("Repository description:", repository.data.description)


asyncio.get_event_loop().run_until_complete(with_token())
```

## Usage notes

- When constructing the client, you should pass a `client_name` parameter, or a user agent string.
- Each response object has a `etag` attribute, which can be used to make subsequent requests.
    - If you pass a `etag` parameter, and the API returns a 304 Not Modified, the client will raise `GitHubNotModifiedException`