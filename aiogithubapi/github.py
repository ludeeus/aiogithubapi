"""AIOGitHubAPI: AIOGitHubAPI"""
from __future__ import annotations

import os
from typing import Any, Dict

import aiohttp

from .client import GitHubClient
from .const import GitHubClientKwarg, GitHubRequestKwarg, HttpMethod, RepositoryType
from .legacy.github import AIOGitHubAPI as LegacyAIOGitHubAPI
from .models.base import GitHubBase
from .models.meta import GitHubMetaModel
from .models.rate_limit import GitHubRateLimitModel
from .models.response import GitHubResponseModel
from .namespaces.orgs import GitHubOrgsNamespace
from .namespaces.projects import GitHubBaseProjectsNamespace
from .namespaces.repos import GitHubReposNamespace
from .namespaces.user import GitHubUserNamespace
from .namespaces.users import GitHubUsersNamespace


class AIOGitHubAPI(LegacyAIOGitHubAPI):
    """Dummy class to not break existing code."""


class GitHub(GitHubBase):
    """
    GitHub

    This is the main class this is where it all starts.
    """

    _close_session = False

    def __init__(
        self,
        token: str = None,
        session: aiohttp.ClientSession = None,
        *,
        api_version: str | None = None,
        **kwargs: Dict[GitHubClientKwarg, Any],
    ) -> None:
        """
        Initialise GitHub API client.

        **Arguments**:

        `token` (Optional)

        Your GitHub [Personal Access Token](https://github.com/settings/tokens).
        Defaults to getting the token from the GITHUB_TOKEN env variable.

        `session` (Optional)

        `aiohttp.ClientSession` to be used by this package.
        If you do not pass one, one will be created for you.

        `**kwargs` (Optional)

        Pass additional arguments.
        See the `aiogithubapi.const.GitHubClientKwarg` enum for valid options.
        """
        if session is None:
            session = aiohttp.ClientSession()
            self._close_session = True

        if token is None:
            token = os.getenv("GITHUB_TOKEN")

        self._session = session
        self._client = GitHubClient(token=token, session=session, api_version=api_version, **kwargs)

        # Namespaces
        self._repos = GitHubReposNamespace(self._client)
        self._user = GitHubUserNamespace(self._client)
        self._users = GitHubUsersNamespace(self._client)
        self._orgs = GitHubOrgsNamespace(self._client)
        self._projects = GitHubBaseProjectsNamespace(self._client)

    @property
    def repos(self) -> GitHubReposNamespace:
        """Property to access the repos namespace."""
        return self._repos

    @property
    def users(self) -> GitHubUsersNamespace:
        """Property to access the users namespace."""
        return self._users

    @property
    def user(self) -> GitHubUserNamespace:
        """Property to access the user namespace."""
        return self._user

    @property
    def orgs(self) -> GitHubOrgsNamespace:
        """Property to access the orgs namespace."""
        return self._orgs

    @property
    def projects(self) -> GitHubBaseProjectsNamespace:
        """Property to access the base projects namespace."""
        return self._projects

    async def __aenter__(self) -> GitHub:
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.repos.events.unsubscribe_all()
        await self.close_session()

    async def close_session(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def generic(
        self,
        endpoint: str,
        data: Dict[str, Any] | str | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[Any]:
        """
         Generic REST API call

         This can be used to call any API endpoint.
         Usefull when you need something that does not have a dedicated method.

         Returns a `aiogithubapi.models.response.GitHubResponseModel` object,
         where the data attribute contains the non-typed response.

         **Arguments**:

         `endpoint`

         The API endpoint to call.
        https://docs.github.com/en/rest
        """
        return await self._client.async_call_api(endpoint=endpoint, data=data, **kwargs)

    async def emojis(
        self,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[Dict[str, str]]:
        """
        Get emojis
        Lists all the emojis available to use on GitHub.

        https://docs.github.com/en/rest/reference/emojis#get-emojis
        """
        return await self._client.async_call_api(endpoint="/emojis", **kwargs)

    async def versions(
        self,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[str]]:
        """
        Get all supported GitHub API versions.

        https://docs.github.com/en/rest/meta#get-all-api-versions
        """
        return await self._client.async_call_api(endpoint="/versions", **kwargs)

    async def markdown(
        self,
        text: str,
        *,
        mode: str | None = None,
        context: RepositoryType | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[str]:
        """
         Render a Markdown document

         **Arguments**:

         `text`

         The Markdown text to render in HTML.

         `mode`

         The rendering mode to use. Defaults to 'markdown'.
         If context is provided this will be set to 'gfm'.

         `context`

         The repository context to render the Markdown in.

        https://docs.github.com/en/rest/reference/markdown#render-a-markdown-document
        """
        return await self._client.async_call_api(
            endpoint="/markdown",
            data={"text": text, "mode": "gfm" if context else mode, "context": context},
            **{**kwargs, GitHubRequestKwarg.METHOD: HttpMethod.POST},
        )

    async def meta(
        self,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubMetaModel]:
        """
        Returns meta information about GitHub, including a list of GitHub's IP addresses.

        https://docs.github.com/en/rest/reference/meta#get-github-meta-information
        """
        response = await self._client.async_call_api(endpoint="/meta", **kwargs)
        response.data = GitHubMetaModel(response.data)
        return response

    async def zen(self, **kwargs: Dict[GitHubRequestKwarg, Any]) -> GitHubResponseModel[str]:
        """
        ZEN

        https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#hello-world
        """
        return await self._client.async_call_api(endpoint="/zen", **kwargs)

    async def octocat(self, **kwargs: Dict[GitHubRequestKwarg, Any]) -> GitHubResponseModel[str]:
        """
        Get the octocat as ASCII art

        https://docs.github.com/en/rest/reference/meta#get-octocat
        """
        return await self._client.async_call_api(endpoint="/octocat", **kwargs)

    async def rate_limit(
        self,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubRateLimitModel]:
        """
        Get rate limit status for the authenticated user

        https://docs.github.com/en/rest/reference/rate-limit#get-rate-limit-status-for-the-authenticated-user
        """
        response = await self._client.async_call_api(endpoint="/rate_limit", **kwargs)
        response.data = GitHubRateLimitModel(response.data)
        return response

    async def graphql(
        self,
        query: str,
        variables: Dict[str, Any] | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[dict]:
        """
        Use the GitHub GraphQL API

        https://docs.github.com/en/graphql
        """
        return await self._client.async_call_api(
            endpoint="/graphql",
            data={"query": query, "variables": variables or {}},
            method=HttpMethod.POST,
            **kwargs,
        )
