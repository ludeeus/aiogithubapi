# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import datetime
import json

import pytest

from aiogithubapi import GitHub
from tests.const import NOT_RATELIMITED, TOKEN
from tests.responses.contents import contents_file_response
from tests.responses.repository_fixture import repository_response
from tests.responses.tree import tree_response


@pytest.mark.asyncio
async def test_tree_content(aresponses, repository_response, tree_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/git/trees/master",
        "get",
        aresponses.Response(
            text=json.dumps(tree_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        contents = await repository.get_tree("master")
        assert len([x for x in contents if x.is_directory]) == 1
        assert contents[0].full_path == "subdir/file.txt"
        assert not contents[0].is_directory
        assert contents[0].path == "subdir"
        assert contents[0].filename == "file.txt"
        assert (
            contents[0].url
            == "https://api.github.com/repos/octocat/Hello-World/git/7c258a9869f33c1e1e1f74fbb32f07c86cb5a75b"
        )
        assert (
            contents[0].download_url
            == "https://raw.githubusercontent.com/octocat/Hello-World/master/subdir/file.txt"
        )


@pytest.mark.asyncio
async def test_content(aresponses, repository_response, contents_file_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/contents/README.md",
        "get",
        aresponses.Response(
            text=json.dumps(contents_file_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        content = await repository.get_contents("README.md", "master")
        assert content.type == "file"
        assert content.encoding == "base64"
        assert content.name == "README.md"
        assert content.path == "README.md"
        assert content.content == ""
        assert (
            content.download_url
            == "https://raw.githubusercontent.com/octokit/octokit.rb/master/README.md"
        )
