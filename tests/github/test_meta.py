"""Test meta."""
# pylint: disable=missing-docstring
import pytest

from aiogithubapi import GitHubAPI

from tests.common import MockedRequests


@pytest.mark.asyncio
async def test_meta(github_api: GitHubAPI, mock_requests: MockedRequests):
    response = await github_api.meta()
    assert response.status == 200
    assert response.data.verifiable_password_authentication
    assert (
        response.data.ssh_key_fingerprints.sha256_ed25519
        == "+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU"
    )
    assert mock_requests.called == 1
    assert mock_requests.last_request["url"] == "https://api.github.com/meta"
