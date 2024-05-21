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
from ..models.tag import GitHubTagModel
from .base import BaseNamespace
from .contents import GitHubContentsNamespace
from .events import GitHubEventsReposNamespace
from .git import GitHubGitNamespace
from .issues import GitHubIssuesNamespace
from .projects import GitHubRepositoryProjectsNamespace
from .pulls import GitHubPullsNamespace
from .releases import GitHubReleasesNamespace
from .traffic import GitHubTrafficNamespace


class GitHubReposNamespace(BaseNamespace):
    """Methods for the repos namespace"""

    def __post_init__(self) -> None:
        self._contents = GitHubContentsNamespace(self._client)
        self._events = GitHubEventsReposNamespace(self._client)
        self._git = GitHubGitNamespace(self._client)
        self._issues = GitHubIssuesNamespace(self._client)
        self._pulls = GitHubPullsNamespace(self._client)
        self._releases = GitHubReleasesNamespace(self._client)
        self._traffic = GitHubTrafficNamespace(self._client)
        self._projects = GitHubRepositoryProjectsNamespace(self._client)

    @property
    def projects(self) -> GitHubRepositoryProjectsNamespace:
        """Property to access the users projects namespace"""
        return self._projects

    @property
    def contents(self) -> GitHubContentsNamespace:
        """Property to access the contents namespace"""
        return self._contents

    @property
    def events(self) -> GitHubEventsReposNamespace:
        """Property to access the events namespace"""
        return self._events

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
        *,
        sha: str | None = None,
        path: str | None = None,
        author: str | None = None,
        since: str | None = None,
        until: str | None = None,
        per_page: int = 30,
        page: int = 0,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[List[GitHubCommitModel]]:
        """
        List commits from a repository.

        **Arguments**:

        - `repository`: The repository to return commits from, specified as
            `<owner>/<repository>`, e.g. "octocat/hello-world".
        - `sha`: Filter the commits to only those with the given SHA.
        - `path`: Filter the commits to only those with changes to the given path.
        - `author`: Filter the commits to only those with the given author.
        - `since`: Filter the commits to only those that were made after the given
            date and time. The `since` parameter should be formatted as an ISO 8601
            date and time, e.g. "2022-12-03T12:34:56Z".
        - `until`: Filter the commits to only those that were made before the given
            date and time. The `until` parameter should be formatted as an ISO 8601
            date and time, e.g. "2022-12-03T12:34:56Z".
        - `per_page`: The number of commits to return per page. The default value is
            30 and the maximum allowed value is 100.
        - `page`: The page number to return. The default value is 0 (the first page).

        For more details, see the API documentation at:
        https://docs.github.com/en/rest/reference/repos#list-commits
        """
        params = {
            "per_page": per_page,
            "page": page,
        }

        if sha is not None:
            params["sha"] = sha
        if path is not None:
            params["path"] = path
        if author is not None:
            params["author"] = author
        if since is not None:
            params["since"] = since
        if until is not None:
            params["until"] = until

        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/commits",
            params=params,
            **kwargs,
        )
        response.data = [GitHubCommitModel(data) for data in response.data]
        return response

    async def list_tags(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[List[GitHubTagModel]]:
        """
         List tags

         **Arguments**:

         `repository`

         The repository to return tags from, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/repos#list-repository-tags
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/tags",
            **kwargs,
        )
        response.data = [GitHubTagModel(data) for data in response.data]
        return response

    async def tarball(
        self,
        repository: RepositoryType,
        *,
        ref: str | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[bytes]:
        """
         Download a repository archive (tar)

         **Arguments**:

         `repository`

         The repository to return the tar from, example "octocat/hello-world"

         `ref`

         The name of the commit/branch/tag. Default: the repository's default branch (usually main)

        https://docs.github.com/en/rest/reference/repos#download-a-repository-archive-tar
        """

        return await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/tarball/{ref or ''}",
            **kwargs,
        )

    async def zipball(
        self,
        repository: RepositoryType,
        *,
        ref: str | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[bytes]:
        """
         Download a repository archive (zip)

         **Arguments**:

         `repository`

         The repository to return the zip from, example "octocat/hello-world"

         `ref`

         The name of the commit/branch/tag. Default: the repository's default branch (usually main)

        https://docs.github.com/en/rest/reference/repos#download-a-repository-archive-zip
        """

        return await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/zipball/{ref or ''}",
            **kwargs,
        )

    async def readme(
        self,
        repository: RepositoryType,
        *,
        dir: str | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[str]:
        """
         Gets the preferred README for a repository.

         **Arguments**:

         `repository`

         The repository to return the zip from, example "octocat/hello-world"

         `dir`

         The alternate path to look for a README file

        https://docs.github.com/en/rest/reference/repos#download-a-repository-archive-zip
        """

        return await self._client.async_call_api(
            endpoint=f"/repos/{repository_full_name(repository)}/readme/{dir or ''}",
            **kwargs,
        )
