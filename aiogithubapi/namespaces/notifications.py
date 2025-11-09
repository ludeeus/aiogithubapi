"""
Methods for the notifications namespace

https://docs.github.com/en/rest/activity/notifications
"""

from __future__ import annotations

from typing import Any

from ..const import GitHubRequestKwarg
from ..models.notification import GitHubNotificationModel
from ..models.response import GitHubResponseModel
from .base import BaseNamespace


class GitHubNotificationsNamespace(BaseNamespace):
    """Methods for the notifications namespace"""

    async def list(
        self,
        *,
        all: bool = False,
        participating: bool = False,
        since: str | None = None,
        before: str | None = None,
        page: int = 1,
        per_page: int = 50,
        params: dict[str, str] | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> GitHubResponseModel[list[GitHubNotificationModel]]:
        """
        List notifications for the authenticated user

        https://docs.github.com/en/rest/activity/notifications#list-notifications-for-the-authenticated-user
        """
        request_params = {}
        if all:
            request_params["all"] = "true"
        if participating:
            request_params["participating"] = "true"
        if since:
            request_params["since"] = since
        if before:
            request_params["before"] = before
        if page != 1:
            request_params["page"] = str(page)
        if per_page != 50:
            request_params["per_page"] = str(per_page)
        if params:
            request_params.update(params)

        response = await self._client.async_call_api(
            endpoint="/notifications",
            params=request_params,
            **kwargs,
        )
        response.data = [GitHubNotificationModel(data) for data in response.data]
        return response
