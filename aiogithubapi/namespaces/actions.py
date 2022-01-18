"""
Methods for the actions namespace

https://docs.github.com/en/rest/reference/actions
"""
from __future__ import annotations

from typing import Any, Dict

from ..const import GitHubRequestKwarg, RepositoryType
from ..models.response import GitHubResponseModel
from ..models.workflows import GitHubWorkflowsModel
from .base import BaseNamespace


class GitHubActionsNamespace(BaseNamespace):
    """Methods for the actions namespace"""

    async def workflows(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubWorkflowsModel]:
        """
        Get repository action workflows

        Get a list of worflows

         **Arguments**:

         `repository`

         The repository to return workflows for, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/actions#workflows
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository}/actions/workflows",
            **kwargs,
        )
        response.data = GitHubWorkflowsModel(response.data)
        return response
