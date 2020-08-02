 
"""
Generated by generate/generate.py - 2020-08-02 10:35:28.920747
"""
from aiogithubapi.objects.users.user import AIOGitHubAPIUsersUser
from tests.responses.users.user_fixtrue import user_fixtrue_response


def test_user(user_fixtrue_response):
    obj = AIOGitHubAPIUsersUser(user_fixtrue_response)
    assert obj.login == user_fixtrue_response["login"]
    assert obj.id == user_fixtrue_response["id"]
    assert obj.node_id == user_fixtrue_response["node_id"]
    assert obj.avatar_url == user_fixtrue_response["avatar_url"]
    assert obj.gravatar_id == user_fixtrue_response["gravatar_id"]
    assert obj.url == user_fixtrue_response["url"]
    assert obj.html_url == user_fixtrue_response["html_url"]
    assert obj.followers_url == user_fixtrue_response["followers_url"]
    assert obj.following_url == user_fixtrue_response["following_url"]
    assert obj.gists_url == user_fixtrue_response["gists_url"]
    assert obj.starred_url == user_fixtrue_response["starred_url"]
    assert obj.subscriptions_url == user_fixtrue_response["subscriptions_url"]
    assert obj.organizations_url == user_fixtrue_response["organizations_url"]
    assert obj.repos_url == user_fixtrue_response["repos_url"]
    assert obj.events_url == user_fixtrue_response["events_url"]
    assert obj.received_events_url == user_fixtrue_response["received_events_url"]
    assert obj.type == user_fixtrue_response["type"]
    assert obj.site_admin == user_fixtrue_response["site_admin"]
    assert obj.name == user_fixtrue_response["name"]
    assert obj.company == user_fixtrue_response["company"]
    assert obj.blog == user_fixtrue_response["blog"]
    assert obj.location == user_fixtrue_response["location"]
    assert obj.email == user_fixtrue_response["email"]
    assert obj.hireable == user_fixtrue_response["hireable"]
    assert obj.bio == user_fixtrue_response["bio"]
    assert obj.twitter_username == user_fixtrue_response["twitter_username"]
    assert obj.public_repos == user_fixtrue_response["public_repos"]
    assert obj.public_gists == user_fixtrue_response["public_gists"]
    assert obj.followers == user_fixtrue_response["followers"]
    assert obj.following == user_fixtrue_response["following"]
    assert obj.created_at == user_fixtrue_response["created_at"]
    assert obj.updated_at == user_fixtrue_response["updated_at"]
