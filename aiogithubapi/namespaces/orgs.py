"""
Methods for the orgs namespace

https://docs.github.com/en/rest/reference/orgs
"""
from __future__ import annotations

from typing import Any, Dict

from ..const import GitHubRequestKwarg, HttpMethod
from ..models.organization import (
    GitHubOrganizationMinimalModel,
    GitHubOrganizationModel,
)
from ..models.response import GitHubResponseModel
from .base import BaseNamespace


class GitHubOrgsNamespace(BaseNamespace):
    """Methods for the orgs namespace"""

    async def list(
        self,
        *,
        since: int | None = None,
        per_page: int | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubOrganizationMinimalModel]]:
        """
         List organizations

         **Arguments**:

         `since`

         An organization ID. Only return organizations with an ID greater than this ID.

         `per_page`

         Results per page (max 100) Default: `30`

        https://docs.github.com/en/rest/reference/orgs#list-organizations
        """
        if since is not None:
            kwargs["query"] = {**kwargs.get("query", {}), "since": since}
        if per_page is not None:
            kwargs["query"] = {**kwargs.get("query", {}), "per_page": per_page}

        response = await self._client.async_call_api(
            endpoint="/organizations",
            **kwargs,
        )
        response.data = [GitHubOrganizationMinimalModel(org) for org in response.data or []]
        return response

    async def get(
        self,
        org: str,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubOrganizationModel]:
        """
         Get a organization

         **Arguments**:

         `org`

         The organization to return, example "octocat"

        https://docs.github.com/en/rest/reference/orgs#get-an-organization
        """
        response = await self._client.async_call_api(
            endpoint=f"/orgs/{org}",
            **kwargs,
        )
        response.data = GitHubOrganizationModel(response.data)
        return response

    async def update(
        self,
        org: str,
        data: dict[str, Any],
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubOrganizationModel]:
        """
         Update an organization

         **Arguments**:

         `org`

         The organization to update, example "octocat"

         `data`

         A dictionary of data to update.

        https://docs.github.com/en/rest/reference/orgs#update-an-organization
        """
        response = await self._client.async_call_api(
            endpoint=f"/orgs/{org}",
            data=data,
            method=HttpMethod.PATCH,
            **kwargs,
        )
        response.data = GitHubOrganizationModel(response.data)
        return response
