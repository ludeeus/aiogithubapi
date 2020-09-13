import aiohttp
from tests.common import load_fixture
from tests.const import NOT_RATELIMITED
import pytest
from aiogithubapi import GitHubDevice


@pytest.mark.asyncio
async def test_session():
    async with aiohttp.ClientSession() as session:
        device = GitHubDevice("xxxxx", "", session)
        assert device.session == session


@pytest.mark.asyncio
async def test_device(aresponses, github_device: GitHubDevice):
    aresponses.add(
        "github.com",
        "/login/device/code",
        "post",
        aresponses.Response(
            text=load_fixture("device_code.json"),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "github.com",
        "/login/oauth/access_token",
        "post",
        aresponses.Response(
            text=load_fixture("oauth_access_token_pending.json"),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "github.com",
        "/login/oauth/access_token",
        "post",
        aresponses.Response(
            text=load_fixture("oauth_access_token.json"),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    device = await github_device.async_register_device()
    assert device.user_code == "WDJB-MJHT"

    activation = await github_device.async_device_activation()
    assert activation.access_token == "e72e16c7e42f292c6912e7710c838347ae178b4a"
