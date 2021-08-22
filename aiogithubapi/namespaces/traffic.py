"""
Methods for the traffic namespace

https://docs.github.com/en/rest/reference/repos#traffic
"""
from __future__ import annotations

from typing import Any, Dict

from ..const import GitHubRequestKwarg, RepositoryType
from ..models.clones import GitHubClonesModel
from ..models.response import GitHubResponseModel
from ..models.views import GitHubViewsModel
from .base import BaseNamespace


class GitHubTrafficNamespace(BaseNamespace):
    """Methods for the traffic namespace"""

    async def clones(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubClonesModel]:
        """
        Get repository clones

        Get the total number of clones and breakdown per day or week for the last 14 days.
        Timestamps are aligned to UTC midnight of the beginning of the day or week.
        Week begins on Monday.

         **Arguments**:

         `repository`

         The repository to return clones for, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/git#get-a-tree
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository}/traffic/clones",
            **kwargs,
        )
        response.data = GitHubClonesModel(response.data)
        return response

    async def views(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubViewsModel]:
        """
        Get page views

        Get the total number of views and breakdown per day or week for the last 14 days.
        Timestamps are aligned to UTC midnight of the beginning of the day or week.
        Week begins on Monday.

         **Arguments**:

         `repository`

         The repository to return views for, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/git#get-a-tree
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository}/traffic/views",
            **kwargs,
        )
        response.data = GitHubViewsModel(response.data)
        return response
