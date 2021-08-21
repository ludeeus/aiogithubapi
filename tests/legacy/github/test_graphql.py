# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import pytest

from aiogithubapi import GitHub
from tests.common import TOKEN, load_fixture


@pytest.mark.asyncio
async def test_graphql(client_session):
    async with GitHub(TOKEN, session=client_session) as github:
        repository = await github.graphql(
            query='query{repository(owner: "awesome", name: "repo"){description}}'
        )
        assert repository["repository"]["description"] == "This your first repo!"
