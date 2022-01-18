"""
Methods for the actions namespace

https://docs.github.com/en/rest/reference/actions
"""
from __future__ import annotations

from typing import Any, Dict

from ..const import GitHubRequestKwarg, RepositoryType
from ..models.response import GitHubResponseModel
from ..models.workflow_runs import GitHubWorkflowRunsModel
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

    async def workflow_runs(
        self,
        repository: RepositoryType,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubWorkflowRunsModel]:
        """
        Get repository action workflow runs

        Get a list of worflow runs for a repository

         **Arguments**:

         `repository`

         The repository to return workflows for, example "octocat/hello-world"

        https://docs.github.com/en/rest/reference/actions#list-workflow-runs-for-a-repository
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository}/actions/runs",
            **kwargs,
        )
        response.data = GitHubWorkflowRunsModel(response.data)
        return response

    async def workflow_runs_for_id(
        self,
        repository: RepositoryType,
        workflow_id: int,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[GitHubWorkflowRunsModel]:
        """
        Get repository action workflow runs

        Get a list of worflow runs for a specific workflow

         **Arguments**:

         `repository`

         The repository to return workflows for, example "octocat/hello-world"

         `workflow_id`

         The workflow id to return runs for

        https://docs.github.com/en/rest/reference/actions#list-workflow-runs
        """
        response = await self._client.async_call_api(
            endpoint=f"/repos/{repository}/actions/workflows/{workflow_id}/runs",
            **kwargs,
        )
        response.data = GitHubWorkflowRunsModel(response.data)
        return response
