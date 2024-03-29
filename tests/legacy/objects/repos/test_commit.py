"""
Generated by generate/generate.py - 2020-08-02 15:48:55.441838
"""
from aiogithubapi.objects.repos.commit import AIOGitHubAPIReposCommit

from tests.legacy.responses.repos.commit_fixtrue import commit_fixtrue_response


def test_commit(commit_fixtrue_response):
    obj = AIOGitHubAPIReposCommit(commit_fixtrue_response)
    assert obj.url == commit_fixtrue_response["url"]
    assert obj.sha == commit_fixtrue_response["sha"]
    assert obj.node_id == commit_fixtrue_response["node_id"]
    assert obj.html_url == commit_fixtrue_response["html_url"]
    assert obj.comments_url == commit_fixtrue_response["comments_url"]
    assert obj.commit.url == commit_fixtrue_response["commit"]["url"]
    assert obj.commit.author.name == commit_fixtrue_response["commit"]["author"]["name"]
    assert obj.commit.author.email == commit_fixtrue_response["commit"]["author"]["email"]
    assert obj.commit.author.date == commit_fixtrue_response["commit"]["author"]["date"]
    assert obj.commit.committer.name == commit_fixtrue_response["commit"]["committer"]["name"]
    assert obj.commit.committer.email == commit_fixtrue_response["commit"]["committer"]["email"]
    assert obj.commit.committer.date == commit_fixtrue_response["commit"]["committer"]["date"]
    assert obj.commit.message == commit_fixtrue_response["commit"]["message"]
    assert obj.commit.tree.url == commit_fixtrue_response["commit"]["tree"]["url"]
    assert obj.commit.tree.sha == commit_fixtrue_response["commit"]["tree"]["sha"]
    assert obj.commit.comment_count == commit_fixtrue_response["commit"]["comment_count"]
    assert (
        obj.commit.verification.verified
        == commit_fixtrue_response["commit"]["verification"]["verified"]
    )
    assert (
        obj.commit.verification.reason
        == commit_fixtrue_response["commit"]["verification"]["reason"]
    )
    assert (
        obj.commit.verification.signature
        == commit_fixtrue_response["commit"]["verification"]["signature"]
    )
    assert (
        obj.commit.verification.payload
        == commit_fixtrue_response["commit"]["verification"]["payload"]
    )
    assert obj.author.login == commit_fixtrue_response["author"]["login"]
    assert obj.author.id == commit_fixtrue_response["author"]["id"]
    assert obj.author.node_id == commit_fixtrue_response["author"]["node_id"]
    assert obj.author.avatar_url == commit_fixtrue_response["author"]["avatar_url"]
    assert obj.author.gravatar_id == commit_fixtrue_response["author"]["gravatar_id"]
    assert obj.author.url == commit_fixtrue_response["author"]["url"]
    assert obj.author.html_url == commit_fixtrue_response["author"]["html_url"]
    assert obj.author.followers_url == commit_fixtrue_response["author"]["followers_url"]
    assert obj.author.following_url == commit_fixtrue_response["author"]["following_url"]
    assert obj.author.gists_url == commit_fixtrue_response["author"]["gists_url"]
    assert obj.author.starred_url == commit_fixtrue_response["author"]["starred_url"]
    assert obj.author.subscriptions_url == commit_fixtrue_response["author"]["subscriptions_url"]
    assert obj.author.organizations_url == commit_fixtrue_response["author"]["organizations_url"]
    assert obj.author.repos_url == commit_fixtrue_response["author"]["repos_url"]
    assert obj.author.events_url == commit_fixtrue_response["author"]["events_url"]
    assert (
        obj.author.received_events_url == commit_fixtrue_response["author"]["received_events_url"]
    )
    assert obj.author.type == commit_fixtrue_response["author"]["type"]
    assert obj.author.site_admin == commit_fixtrue_response["author"]["site_admin"]
    assert obj.committer.login == commit_fixtrue_response["committer"]["login"]
    assert obj.committer.id == commit_fixtrue_response["committer"]["id"]
    assert obj.committer.node_id == commit_fixtrue_response["committer"]["node_id"]
    assert obj.committer.avatar_url == commit_fixtrue_response["committer"]["avatar_url"]
    assert obj.committer.gravatar_id == commit_fixtrue_response["committer"]["gravatar_id"]
    assert obj.committer.url == commit_fixtrue_response["committer"]["url"]
    assert obj.committer.html_url == commit_fixtrue_response["committer"]["html_url"]
    assert obj.committer.followers_url == commit_fixtrue_response["committer"]["followers_url"]
    assert obj.committer.following_url == commit_fixtrue_response["committer"]["following_url"]
    assert obj.committer.gists_url == commit_fixtrue_response["committer"]["gists_url"]
    assert obj.committer.starred_url == commit_fixtrue_response["committer"]["starred_url"]
    assert (
        obj.committer.subscriptions_url == commit_fixtrue_response["committer"]["subscriptions_url"]
    )
    assert (
        obj.committer.organizations_url == commit_fixtrue_response["committer"]["organizations_url"]
    )
    assert obj.committer.repos_url == commit_fixtrue_response["committer"]["repos_url"]
    assert obj.committer.events_url == commit_fixtrue_response["committer"]["events_url"]
    assert (
        obj.committer.received_events_url
        == commit_fixtrue_response["committer"]["received_events_url"]
    )
    assert obj.committer.type == commit_fixtrue_response["committer"]["type"]
    assert obj.committer.site_admin == commit_fixtrue_response["committer"]["site_admin"]
    assert obj.parents[0].url == commit_fixtrue_response["parents"][0]["url"]
    assert obj.parents[0].sha == commit_fixtrue_response["parents"][0]["sha"]
    assert obj.stats.additions == commit_fixtrue_response["stats"]["additions"]
    assert obj.stats.deletions == commit_fixtrue_response["stats"]["deletions"]
    assert obj.stats.total == commit_fixtrue_response["stats"]["total"]
    assert obj.files[0].filename == commit_fixtrue_response["files"][0]["filename"]
    assert obj.files[0].additions == commit_fixtrue_response["files"][0]["additions"]
    assert obj.files[0].deletions == commit_fixtrue_response["files"][0]["deletions"]
    assert obj.files[0].changes == commit_fixtrue_response["files"][0]["changes"]
    assert obj.files[0].status == commit_fixtrue_response["files"][0]["status"]
    assert obj.files[0].raw_url == commit_fixtrue_response["files"][0]["raw_url"]
    assert obj.files[0].blob_url == commit_fixtrue_response["files"][0]["blob_url"]
    assert obj.files[0].patch == commit_fixtrue_response["files"][0]["patch"]
