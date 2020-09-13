"""
AIOGitHubAPI: AIOGitHubAPI

Asynchronous Python client for the GitHub API
https://github.com/ludeeus/aiogithubapi
"""
from aiogithubapi.github import AIOGitHubAPI as GitHub
from aiogithubapi.device import AIOGitHubAPIDeviceLogin as GitHubDevice

from aiogithubapi.common.exceptions import (
    AIOGitHubAPIAuthenticationException,
    AIOGitHubAPIException,
    AIOGitHubAPIRatelimitException,
)
