# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import pytest

from aiogithubapi import GitHub
from tests.common import load_fixture
from tests.const import NOT_RATELIMITED, TOKEN


@pytest.mark.asyncio
async def test_graphql(aresponses):
    aresponses.add(
        "api.github.com",
        "/graphql",
        "post",
        aresponses.Response(
            text=load_fixture("gql_simple.json"),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        repository = await github.graphql(
            query='query{repository(owner: "awesome", name: "repo"){description}}'
        )
        assert repository["repository"]["description"] == "This your first repo!"


@pytest.mark.asyncio
async def test_graphql_variable(aresponses):
    aresponses.add(
        "api.github.com",
        "/graphql",
        "post",
        aresponses.Response(
            text=load_fixture("gql_simple.json"),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        repository = await github.graphql(
            query="query($owner: String!, $repo: String!){repository(owner: $owner, name: $repo){description}}",
            variables={"repo": "awesome", "name": "repo"},
        )
        assert repository["repository"]["description"] == "This your first repo!"
