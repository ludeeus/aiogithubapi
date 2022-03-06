"""
Methods for the users namespace

https://docs.github.com/en/rest/reference/users
"""
from __future__ import annotations

from typing import Any, Dict

from ..const import GitHubRequestKwarg
from ..models.organization import GitHubOrganizationMinimalModel
from ..models.repository import GitHubRepositoryModel
from ..models.response import GitHubResponseModel
from ..models.user import GitHubUserModel
from .base import BaseNamespace
from .projects import GitHubUsersProjectsNamespace


class GitHubUsersNamespace(BaseNamespace):
    """Methods for the users namespace"""

    def __post_init__(self) -> None:
        self._projects = GitHubUsersProjectsNamespace(self._client)

    @property
    def projects(self) -> GitHubUsersProjectsNamespace:
        """Property to access the users projects namespace"""
        return self._projects

    async def get(
        self,
        username: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubUserModel]:
        """
         Get a user

         **Arguments**:

         `username`

         The username to return, example "octocat"

        https://docs.github.com/en/rest/reference/users#get-a-user
        """
        response = await self._client.async_call_api(
            endpoint=f"/users/{username}",
            **kwargs,
        )
        response.data = GitHubUserModel(response.data)

        return response

    async def starred(
        self,
        username: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubRepositoryModel]]:
        """
         Get the starred repositories of a user

         **Arguments**:

         `username`

         The username to return, example "octocat"


        https://docs.github.com/en/rest/reference/users#get-a-user
        """
        response = await self._client.async_call_api(
            endpoint=f"/users/{username}/starred",
            **kwargs,
        )

        response.data = [GitHubRepositoryModel(data) for data in response.data]

        return response

    async def repos(
        self,
        username: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubRepositoryModel]]:
        """
         Get the repositories of a user

         **Arguments**:

         `username`

         The username to return, example "octocat"


        https://docs.github.com/en/rest/reference/repos#list-repositories-for-a-user
        """
        response = await self._client.async_call_api(
            endpoint=f"/users/{username}/repos",
            **kwargs,
        )

        response.data = [GitHubRepositoryModel(data) for data in response.data]

        return response

    async def orgs(
        self,
        username: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubOrganizationMinimalModel]]:
        """
         List public organization memberships for the specified user.

         **Arguments**:

         `username`

         The username to return, example "octocat"


        https://docs.github.com/en/rest/reference/orgs#list-organizations-for-a-user
        """
        response = await self._client.async_call_api(
            endpoint=f"/users/{username}/orgs",
            **kwargs,
        )

        response.data = [GitHubOrganizationMinimalModel(data) for data in response.data or []]

        return response
