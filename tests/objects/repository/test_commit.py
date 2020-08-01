# pylint: disable=missing-docstring, redefined-outer-name, unused-import
import datetime
import json
import pytest
from aiogithubapi import GitHub

from tests.const import TOKEN, NOT_RATELIMITED
from tests.responses.repository import repository_response
from tests.responses.commit import commit_response


@pytest.mark.asyncio
async def test_get_last_commit(aresponses, repository_response, commit_response):
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
        "/repos/octocat/Hello-World/branches/master",
        "get",
        aresponses.Response(
            text=json.dumps(commit_response), status=200, headers=NOT_RATELIMITED,
        ),
    )

    async with GitHub(TOKEN) as github:
        repository = await github.get_repo("octocat/Hello-World")
        commit = await repository.get_last_commit()

        assert commit.url == commit_response["url"]
        assert commit.sha == commit_response["sha"]
        assert commit.sha_short == commit_response["sha"][0:7]
        assert commit.node_id == commit_response["node_id"]
        assert commit.html_url == commit_response["html_url"]
        assert commit.comments_url == commit_response["comments_url"]
        assert commit.commit.url == commit_response["commit"]["url"]
        assert commit.commit.author.name == commit_response["commit"]["author"]["name"]
        assert (
            commit.commit.author.email == commit_response["commit"]["author"]["email"]
        )
        assert commit.commit.author.date == commit_response["commit"]["author"]["date"]
        assert (
            commit.commit.committer.name
            == commit_response["commit"]["committer"]["name"]
        )
        assert (
            commit.commit.committer.email
            == commit_response["commit"]["committer"]["email"]
        )
        assert (
            commit.commit.committer.date
            == commit_response["commit"]["committer"]["date"]
        )

        assert commit.commit.message == commit_response["commit"]["message"]
        assert commit.commit.tree.url == commit_response["commit"]["tree"]["url"]
        assert commit.commit.tree.sha == commit_response["commit"]["tree"]["sha"]

        assert commit.commit.comment_count == commit_response["commit"]["comment_count"]

        assert (
            commit.commit.verification.verified
            == commit_response["commit"]["verification"]["verified"]
        )
        assert (
            commit.commit.verification.reason
            == commit_response["commit"]["verification"]["reason"]
        )
        assert (
            commit.commit.verification.signature
            == commit_response["commit"]["verification"]["signature"]
        )
        assert (
            commit.commit.verification.payload
            == commit_response["commit"]["verification"]["payload"]
        )

        assert commit.author.login == commit_response["author"]["login"]
        assert commit.author.id == commit_response["author"]["id"]
        assert commit.author.node_id == commit_response["author"]["node_id"]
        assert commit.author.avatar_url == commit_response["author"]["avatar_url"]
        assert commit.author.gravatar_id == commit_response["author"]["gravatar_id"]
        assert commit.author.url == commit_response["author"]["url"]
        assert commit.author.html_url == commit_response["author"]["html_url"]
        assert commit.author.followers_url == commit_response["author"]["followers_url"]
        assert commit.author.following_url == commit_response["author"]["following_url"]
        assert commit.author.gists_url == commit_response["author"]["gists_url"]
        assert commit.author.starred_url == commit_response["author"]["starred_url"]
        assert (
            commit.author.subscriptions_url
            == commit_response["author"]["subscriptions_url"]
        )
        assert (
            commit.author.organizations_url
            == commit_response["author"]["organizations_url"]
        )
        assert commit.author.repos_url == commit_response["author"]["repos_url"]
        assert commit.author.events_url == commit_response["author"]["events_url"]
        assert (
            commit.author.received_events_url
            == commit_response["author"]["received_events_url"]
        )
        assert commit.author.type == commit_response["author"]["type"]
        assert commit.author.site_admin == commit_response["author"]["site_admin"]

        assert commit.committer.login == commit_response["committer"]["login"]
        assert commit.committer.id == commit_response["committer"]["id"]
        assert commit.committer.node_id == commit_response["committer"]["node_id"]
        assert commit.committer.avatar_url == commit_response["committer"]["avatar_url"]
        assert (
            commit.committer.gravatar_id == commit_response["committer"]["gravatar_id"]
        )
        assert commit.committer.url == commit_response["committer"]["url"]
        assert commit.committer.html_url == commit_response["committer"]["html_url"]
        assert (
            commit.committer.followers_url
            == commit_response["committer"]["followers_url"]
        )
        assert (
            commit.committer.following_url
            == commit_response["committer"]["following_url"]
        )
        assert commit.committer.gists_url == commit_response["committer"]["gists_url"]
        assert (
            commit.committer.starred_url == commit_response["committer"]["starred_url"]
        )
        assert (
            commit.committer.subscriptions_url
            == commit_response["committer"]["subscriptions_url"]
        )
        assert (
            commit.committer.organizations_url
            == commit_response["committer"]["organizations_url"]
        )
        assert commit.committer.repos_url == commit_response["committer"]["repos_url"]
        assert commit.committer.events_url == commit_response["committer"]["events_url"]
        assert (
            commit.committer.received_events_url
            == commit_response["committer"]["received_events_url"]
        )
        assert commit.committer.type == commit_response["committer"]["type"]
        assert commit.committer.site_admin == commit_response["committer"]["site_admin"]

        assert commit.parents[0].url == commit_response["parents"][0]["url"]
        assert commit.parents[0].sha == commit_response["parents"][0]["sha"]

        assert commit.stats.additions == commit_response["stats"]["additions"]
        assert commit.stats.deletions == commit_response["stats"]["deletions"]
        assert commit.stats.total == commit_response["stats"]["total"]

        assert commit.files[0].filename == commit_response["files"][0]["filename"]
        assert commit.files[0].additions == commit_response["files"][0]["additions"]
        assert commit.files[0].deletions == commit_response["files"][0]["deletions"]
        assert commit.files[0].changes == commit_response["files"][0]["changes"]
        assert commit.files[0].status == commit_response["files"][0]["status"]
        assert commit.files[0].raw_url == commit_response["files"][0]["raw_url"]
        assert commit.files[0].blob_url == commit_response["files"][0]["blob_url"]
        assert commit.files[0].patch == commit_response["files"][0]["patch"]
