# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import datetime
import json

import pytest

from aiogithubapi import AIOGitHubAPIException, AIOGitHubAPINotModifiedException, GitHub

from tests.common import TOKEN
from tests.legacy.responses.base import base_response
from tests.legacy.responses.branch import branch_response
from tests.legacy.responses.contents import (
    contents_file_response,
    contents_list_response,
)
from tests.legacy.responses.issue_fixture import issue_response
from tests.legacy.responses.releases import releases_response
from tests.legacy.responses.repository_fixture import repository_response
from tests.legacy.responses.tree import tree_response


@pytest.mark.asyncio
async def test_get_repository(aresponses, repository_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        assert repository.description == "This your first repo!"
        assert repository.id == 1296269
        assert repository.name == "Hello-World"
        assert repository.full_name == "octocat/Hello-World"
        assert repository.pushed_at == datetime.datetime(2011, 1, 26, 19, 6, 43)
        assert not repository.archived
        assert repository.topics == ["octocat", "atom", "electron", "api"]
        assert not repository.fork
        assert repository.forks_count == 9
        assert repository.default_branch == "main"
        assert repository.last_commit is None
        assert repository.homepage == "https://github.com"
        assert repository.stargazers_count == 80
        assert repository.watchers_count == 80
        assert repository.owner.login == "octocat"


@pytest.mark.asyncio
async def test_set_last_commit(aresponses, repository_response, branch_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/branches/main",
        "get",
        aresponses.Response(
            text=json.dumps(branch_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/branches/main",
        "get",
        aresponses.Response(status=304),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        assert repository.last_commit is None
        await repository.set_last_commit()
        assert repository.last_commit == "7fd1a60"

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await repository.set_last_commit(github.client.last_response.etag)


@pytest.mark.asyncio
async def test_get_contents_file(aresponses, repository_response, contents_file_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/contents/README.md",
        "get",
        aresponses.Response(
            text=json.dumps(contents_file_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        contents = await repository.get_contents("README.md", "main")
        assert contents.name == "README.md"


@pytest.mark.asyncio
async def test_get_contents_list(aresponses, repository_response, contents_list_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/contents/",
        "get",
        aresponses.Response(
            text=json.dumps(contents_list_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        contents = await repository.get_contents("", "main")
        assert len(contents) == 2


@pytest.mark.asyncio
async def test_get_tree(aresponses, repository_response, tree_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/git/trees/main",
        "get",
        aresponses.Response(
            text=json.dumps(tree_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        contents = await repository.get_tree("main")
        assert contents[0].full_path == "subdir/file.txt"
        with pytest.raises(AIOGitHubAPIException):
            await repository.get_tree()


@pytest.mark.asyncio
async def test_get_rendered_contents(aresponses, repository_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/contents/README.md",
        "get",
        aresponses.Response(
            text="test",
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/contents/README.md",
        "get",
        aresponses.Response(status=304),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        rendered = await repository.get_rendered_contents("README.md", "main")
        assert rendered == "test"

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await repository.get_rendered_contents(
                "README.md", "main", etag=github.client.last_response.etag
            )


@pytest.mark.asyncio
async def test_get_releases(aresponses, repository_response, releases_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/releases",
        "get",
        aresponses.Response(
            text=json.dumps(releases_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/releases",
        "get",
        aresponses.Response(
            text=json.dumps(releases_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/releases",
        "get",
        aresponses.Response(
            text=json.dumps(releases_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/releases",
        "get",
        aresponses.Response(status=304),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        releases = await repository.get_releases()
        assert len(releases) == 1
        releases = await repository.get_releases(prerelease=True)
        assert len(releases) == 2
        assert releases[0].tag_name == "v1.0.0"
        assert not releases[0].prerelease
        releases = await repository.get_releases(prerelease=True, returnlimit=1)
        assert len(releases) == 1

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await repository.get_releases(etag=github.client.last_response.as_dict()["etag"])


@pytest.mark.asyncio
async def test_get_issue(aresponses, repository_response, issue_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1",
        "get",
        aresponses.Response(
            text=json.dumps(issue_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1",
        "get",
        aresponses.Response(status=304),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        issue = await repository.get_issue(1)
        assert issue.title == "Found a bug"

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await repository.get_issue(1, etag=github.client.last_response.etag)


@pytest.mark.asyncio
async def test_create_issue(aresponses, repository_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues",
        "post",
        aresponses.Response(
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        data = {
            "title": "test",
            "body": "body",
            "state": "closed",
            "milestone": "v1.0",
            "labels": ["test"],
            "assignees": ["octocat"],
        }
        await repository.create_issue(**data)


@pytest.mark.asyncio
async def test_get_last_commit(aresponses, repository_response, branch_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/branches/main",
        "get",
        aresponses.Response(
            text=json.dumps(branch_response),
            status=200,
            headers={
                "X-RateLimit-Remaining": "1337",
                "Content-Type": "application/json",
                "Etag": "xyz..zyx",
            },
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/branches/main",
        "get",
        aresponses.Response(status=304),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        assert repository.last_commit is None
        commit = await repository.get_last_commit()
        assert commit.sha == "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d"

        with pytest.raises(AIOGitHubAPINotModifiedException):
            await repository.get_last_commit(etag=github.client.last_response.etag)
