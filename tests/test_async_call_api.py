import aiohttp
import pytest

from aiogithubapi.helpers import async_call_api
from tests.common import load_fixture
from tests.const import NOT_RATELIMITED


@pytest.mark.asyncio
async def test_async_call_api(aresponses):
    aresponses.add(
        "example.com",
        "/path",
        "get",
        aresponses.Response(
            text=load_fixture("base/response"),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    async with aiohttp.ClientSession() as session:
        req = await async_call_api(session, "GET", "http://example.com/path", {})
        assert isinstance(req.as_dict(), dict)
