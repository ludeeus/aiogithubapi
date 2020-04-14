"""
AIOGitHubAPI: AIOGitHubAPI

Python3 async client for the GitHub API.

https://developer.github.com/v3/
"""
from aiogithubapi.github import AIOGitHubAPI as GitHub

from aiogithubapi.common.exceptions import (
    AIOGitHubAPIAuthenticationException,
    AIOGitHubAPIException,
    AIOGitHubAPIRatelimitException,
)
