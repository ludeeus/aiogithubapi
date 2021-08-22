"""
Methods for the repos namespace

https://docs.github.com/en/rest/reference/repos
"""
from __future__ import annotations

from typing import Any, Dict, List

from ..const import GitHubRequestKwarg, RepositoryType
from ..helpers import repository_full_name
from ..models.commit import GitHubCommitModel
from ..models.repository import GitHubRepositoryModel
from ..models.response import GitHubResponseModel
from .base import BaseNamespace
from .contents import GitHubContentsNamespace
from .git import GitHubGitNamespace
from .issues import GitHubIssuesNamespace
from .pulls import GitHubPullsNamespace
from .releases import GitHubReleasesNamespace
from .traffic import GitHubTrafficNamespace


class GitHubReposNamespace(BaseNamespace):
    """Methods for the repos namespace"""

    def __post_init__(self) -> None:
        self._contents = GitHubContentsNamespace(self._client)
        self._git = GitHubGitNamespace(self._client)
        self._issues = GitHubIssuesNamespace(self._client)
        self._pulls = GitHubPullsNamespace(self._client)
        self._releases = GitHubReleasesNamespace(self._client)
        self._traffic = GitHubTrafficNamespace(self._client)

    @property
    def contents(self) -> GitHubContentsNamespace:
        """Property to access the contents namespace"""
        return self._contents

    @property
    def git(self) -> GitHubGitNamespace:
        """Property to access the git namespace"""
        return self._git

    @property
    def issues(self) -> GitHubIssuesNamespace:
        """Property to access the issues namespace"""
        return self._issues

    @property
    def pulls(self) -> GitHubPullsNamespace:
        """Property to access the pull requests namespace"""
        return self._pulls

    @property
    def releases(self) -> GitHubReleasesNamespace:
        """Property to access the releases namespace"""
        return self._releases

    @property
    def traffic(self) -> GitHubTrafficNamespace:
        """Property to access the traffic namespace"""
        return self._traffic

    async def get(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubRepositoryModel]:
        """
         Get a repository

         **Arguments**:

         `repository`

         The repository to return, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/repos#get-a-repository
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}",
            **kwargs,
        )
        response.data = GitHubRepositoryModel(response.data)
        return response

    async def list_commits(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[List[GitHubCommitModel]]:
        """
         List commits

         **Arguments**:

         `repository`

         The repository to return commits from, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/repos#list-commits
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/commits",
            **kwargs,
        )
        response.data = [GitHubCommitModel(data) for data in response.data]
        return response
