"""
Generated by generate/generate.py - 2020-08-02 10:09:26.842173
"""
from aiogithubapi.objects.repository.collaborator import (
    AIOGitHubAPIRepositoryCollaborator,
)

from tests.legacy.responses.repository.collaborator_fixtrue import (
    collaborator_fixtrue_response,
)


def test_collaborator(collaborator_fixtrue_response):
    obj = AIOGitHubAPIRepositoryCollaborator(collaborator_fixtrue_response)
    assert obj.login == collaborator_fixtrue_response["login"]
    assert obj.id == collaborator_fixtrue_response["id"]
    assert obj.node_id == collaborator_fixtrue_response["node_id"]
    assert obj.avatar_url == collaborator_fixtrue_response["avatar_url"]
    assert obj.gravatar_id == collaborator_fixtrue_response["gravatar_id"]
    assert obj.url == collaborator_fixtrue_response["url"]
    assert obj.html_url == collaborator_fixtrue_response["html_url"]
    assert obj.followers_url == collaborator_fixtrue_response["followers_url"]
    assert obj.following_url == collaborator_fixtrue_response["following_url"]
    assert obj.gists_url == collaborator_fixtrue_response["gists_url"]
    assert obj.starred_url == collaborator_fixtrue_response["starred_url"]
    assert obj.subscriptions_url == collaborator_fixtrue_response["subscriptions_url"]
    assert obj.organizations_url == collaborator_fixtrue_response["organizations_url"]
    assert obj.repos_url == collaborator_fixtrue_response["repos_url"]
    assert obj.events_url == collaborator_fixtrue_response["events_url"]
    assert obj.received_events_url == collaborator_fixtrue_response["received_events_url"]
    assert obj.type == collaborator_fixtrue_response["type"]
    assert obj.site_admin == collaborator_fixtrue_response["site_admin"]
    assert obj.permissions.pull == collaborator_fixtrue_response["permissions"]["pull"]
    assert obj.permissions.push == collaborator_fixtrue_response["permissions"]["push"]
    assert obj.permissions.admin == collaborator_fixtrue_response["permissions"]["admin"]
