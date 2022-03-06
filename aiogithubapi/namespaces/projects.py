"""
Methods for the projects namespace

https://docs.github.com/en/rest/reference/projects
"""
from __future__ import annotations

from typing import Any, Dict

from aiogithubapi.helpers import repository_full_name

from ..const import GitHubRequestKwarg, HttpMethod, RepositoryType
from ..models.projects import GitHubProjectModel
from ..models.response import GitHubResponseModel
from .base import BaseNamespace


class _BaseProjectsNamespace(BaseNamespace):
    """Methods for the base projects namespace"""

    async def _list(
        self,
        endpoint: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubProjectModel]]:
        """Internal helper"""
        response = await self._client.async_call_api(endpoint=endpoint, **kwargs)
        response.data = [GitHubProjectModel(project) for project in response.data or []]
        return response

    async def _get(
        self,
        endpoint: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubProjectModel]:
        """Internal helper"""
        response = await self._client.async_call_api(endpoint=endpoint, **kwargs)
        response.data = GitHubProjectModel(response.data)
        return response

    async def _update(
        self,
        endpoint: str,
        data: dict[str, Any],
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubProjectModel]:
        """Internal helper"""
        response = await self._client.async_call_api(
            endpoint=endpoint,
            data=data,
            method=HttpMethod.PATCH,
            **kwargs,
        )
        response.data = GitHubProjectModel(response.data)
        return response

    async def _create(
        self,
        endpoint: str,
        data: dict[str, Any],
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubProjectModel]:
        """Internal helper"""
        response = await self._client.async_call_api(
            endpoint=endpoint,
            data=data,
            method=HttpMethod.POST,
            **kwargs,
        )
        response.data = GitHubProjectModel(response.data)
        return response

    async def _delete(
        self,
        endpoint: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[None]:
        """Internal helper"""
        return await self._client.async_call_api(
            endpoint=endpoint,
            method=HttpMethod.DELETE,
            **kwargs,
        )


class GitHubBaseProjectsNamespace(_BaseProjectsNamespace):
    """Methods for the organization projects namespace"""

    async def get(
        self,
        project_id: int,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubProjectModel]:
        """
         Get a project

         **Arguments**:

         `project_id`

         The project ID to return

        https://docs.github.com/en/rest/reference/projects#list-organization-projects
        """
        return await super()._get(endpoint=f"/projects/{project_id}", **kwargs)

    async def update(
        self,
        project_id: int,
        data: dict[str, Any],
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubProjectModel]:
        """
         Get a project

         **Arguments**:

         `project_id`

         The project ID to return

         `data`

         A dictionary of the data to update.

        https://docs.github.com/en/rest/reference/projects#update-a-project
        """
        return await super()._update(endpoint=f"/projects/{project_id}", data=data, **kwargs)

    async def delete(
        self,
        project_id: int,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[None]:
        """
         Delete a project

         **Arguments**:

         `project_id`

         The project ID to return

        https://docs.github.com/en/rest/reference/projects#delete-a-project
        """
        return await super()._delete(endpoint=f"/projects/{project_id}", **kwargs)


class GitHubOrganizationProjectsNamespace(_BaseProjectsNamespace):
    """Methods for the organization projects namespace"""

    async def list(
        self,
        org: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubProjectModel]]:
        """
         List organization projects

         **Arguments**:

         `org`

         The organization to return, example "octocat"

        https://docs.github.com/en/rest/reference/projects#list-organization-projects
        """
        return await super()._list(endpoint=f"/orgs/{org}/projects", **kwargs)

    async def create(
        self,
        org: str,
        name: str,
        *,
        body: str | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubProjectModel]:
        """
         List organization projects

         **Arguments**:

         `org`

         The organization to create the project for, example "octocat"

         `name`

         The name of the project.

         `body`

         The description of the project.

        https://docs.github.com/en/rest/reference/projects#create-an-organization-project
        """
        return await super()._create(
            endpoint=f"/orgs/{org}/projects",
            data={"name": name, "body": body},
            **kwargs,
        )


class GitHubRepositoryProjectsNamespace(_BaseProjectsNamespace):
    """Methods for the repository projects namespace"""

    async def list(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubProjectModel]]:
        """
         List repository projects

         **Arguments**:

         `repository`

         The repository to return the zip from, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/projects#list-repository-projects
        """
        return await super()._list(
            endpoint=f"/repos/{repository_full_name(repository)}/projects",
            **kwargs,
        )

    async def create(
        self,
        repository: RepositoryType,
        name: str,
        *,
        body: str | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubProjectModel]:
        """
         Create a new repoitory project

         **Arguments**:

         `repository`

         The repository to return the zip from, example "octocat/hello-world"

         `name`

         The name of the project.

         `body`

         The description of the project.

        https://docs.github.com/en/rest/reference/projects#create-an-organization-project
        """
        return await super()._create(
            endpoint=f"/repos/{repository_full_name(repository)}/projects",
            data={"name": name, "body": body},
            **kwargs,
        )


class GitHubUsersProjectsNamespace(_BaseProjectsNamespace):
    """Methods for the users projects namespace"""

    async def list(
        self,
        username: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubProjectModel]]:
        """
         List user projects

         **Arguments**:

         `username`

         The username to return project from, example "octocat"

        https://docs.github.com/en/rest/reference/projects#list-user-projects
        """
        return await super()._list(endpoint=f"/users/{username}/projects", **kwargs)


class GitHubUserProjectsNamespace(_BaseProjectsNamespace):
    """Methods for the user projects namespace"""

    async def create(
        self,
        name: str,
        *,
        body: str | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubProjectModel]:
        """
         Create a new project for the authenticated user

         **Arguments**:

         `name`

         The name of the project.

         `body`

         The description of the project.

        https://docs.github.com/en/rest/reference/projects#create-a-user-project
        """
        return await super()._create(
            endpoint=f"/user/projects",
            data={"name": name, "body": body},
            **kwargs,
        )
