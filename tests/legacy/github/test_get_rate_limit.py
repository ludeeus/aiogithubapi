# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import pytest

from aiogithubapi import GitHub

from tests.legacy.responses.base import base_response


@pytest.mark.asyncio
async def test_get_rate_limit(mock_response, base_response, github: GitHub):
    mock_response.mock_data = base_response

    rate_limit = await github.get_rate_limit()
    assert rate_limit["remaining"] == "4999"
