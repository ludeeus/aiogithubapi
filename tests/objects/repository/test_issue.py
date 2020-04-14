# pylint: disable=missing-docstring, redefined-outer-name, unused-import

import json
import pytest
from aiogithubapi import GitHub

from tests.const import TOKEN, NOT_RATELIMITED
from tests.responses.repository import repository_response
from tests.responses.issue import issue_response
from tests.responses.issue_comments import issue_comments_response


@pytest.mark.asyncio
async def test_issue(aresponses, repository_response, issue_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1",
        "get",
        aresponses.Response(
            text=json.dumps(issue_response), status=200, headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        issue = await repository.get_issue(1)
        assert issue.html_url == "https://github.com/octocat/Hello-World/issues/1347"
        assert issue.number == 1347
        assert issue.labels == [
            {
                "id": 208045946,
                "node_id": "MDU6TGFiZWwyMDgwNDU5NDY=",
                "url": "https://api.github.com/repos/octocat/Hello-World/labels/bug",
                "name": "bug",
                "description": "Something isn't working",
                "color": "f29513",
                "default": True,
            }
        ]
        assert issue.title == "Found a bug"
        assert issue.state == "open"
        assert issue.assignees == [
            {
                "login": "octocat",
                "id": 1,
                "node_id": "MDQ6VXNlcjE=",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                "gravatar_id": "",
                "url": "https://api.github.com/users/octocat",
                "html_url": "https://github.com/octocat",
                "followers_url": "https://api.github.com/users/octocat/followers",
                "following_url": "https://api.github.com/users/octocat/following{/other_user}",
                "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
                "organizations_url": "https://api.github.com/users/octocat/orgs",
                "repos_url": "https://api.github.com/users/octocat/repos",
                "events_url": "https://api.github.com/users/octocat/events{/privacy}",
                "received_events_url": "https://api.github.com/users/octocat/received_events",
                "type": "User",
                "site_admin": False,
            }
        ]
        assert issue.body == "I'm having a problem with this."
        user = issue.user
        assert user.login == "octocat"
        assert user.id == 1
        assert user.avatar_url == "https://github.com/images/error/octocat_happy.gif"
        assert user.html_url == "https://github.com/octocat"
        assert user.type == "User"
        assert not user.site_admin


@pytest.mark.asyncio
async def test_update_issue(aresponses, repository_response, issue_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1",
        "get",
        aresponses.Response(
            text=json.dumps(issue_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1",
        "post",
        aresponses.Response(status=200, headers=NOT_RATELIMITED,),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        issue = await repository.get_issue(1)
        data = {
            "title": "test",
            "body": "body",
            "state": "closed",
            "milestone": "v1.0",
            "labels": ["test"],
            "assignees": ["octocat"],
        }
        await issue.update(**data)


@pytest.mark.asyncio
async def test_get_issue_comments(
    aresponses, repository_response, issue_response, issue_comments_response
):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1",
        "get",
        aresponses.Response(
            text=json.dumps(issue_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1/comments",
        "get",
        aresponses.Response(
            text=json.dumps(issue_comments_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        issue = await repository.get_issue(1)
        comments = await issue.get_comments()
        assert comments[0].body == "Me too"


@pytest.mark.asyncio
async def test_comment_on_issue(aresponses, repository_response, issue_response):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1",
        "get",
        aresponses.Response(
            text=json.dumps(issue_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1/comments",
        "post",
        aresponses.Response(status=200, headers=NOT_RATELIMITED,),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        issue = await repository.get_issue(1)
        await issue.comment("test")


@pytest.mark.asyncio
async def test_issue_comments(
    aresponses, repository_response, issue_response, issue_comments_response
):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1",
        "get",
        aresponses.Response(
            text=json.dumps(issue_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1/comments",
        "get",
        aresponses.Response(
            text=json.dumps(issue_comments_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        issue = await repository.get_issue(1)
        comments = await issue.get_comments()
        first = comments[0]
        assert (
            first.html_url
            == "https://github.com/octocat/Hello-World/issues/1347#issuecomment-1"
        )
        assert first.body == "Me too"
        assert first.created_at == "2011-04-14T16:00:49Z"
        assert first.updated_at == "2011-04-14T16:00:49Z"
        user = first.user
        assert user.login == "octocat"
        assert user.id == 1
        assert user.avatar_url == "https://github.com/images/error/octocat_happy.gif"
        assert user.html_url == "https://github.com/octocat"
        assert user.type == "User"
        assert not user.site_admin


@pytest.mark.asyncio
async def test_update_issue_comment(
    aresponses, repository_response, issue_response, issue_comments_response
):
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World",
        "get",
        aresponses.Response(
            text=json.dumps(repository_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1",
        "get",
        aresponses.Response(
            text=json.dumps(issue_response), status=200, headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/1/comments",
        "get",
        aresponses.Response(
            text=json.dumps(issue_comments_response),
            status=200,
            headers=NOT_RATELIMITED,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/repos/octocat/Hello-World/issues/comments/1",
        "post",
        aresponses.Response(status=200, headers=NOT_RATELIMITED),
    )
    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        issue = await repository.get_issue(1)
        comments = await issue.get_comments()
        await comments[0].update("test")
