"""
Methods for the events namespace

https://docs.github.com/en/rest/reference/activity#events
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Literal
from uuid import uuid4

from ..const import LOGGER, GitHubRequestKwarg, RepositoryType
from ..exceptions import (
    GitHubAuthenticationException,
    GitHubException,
    GitHubNotFoundException,
    GitHubNotModifiedException,
    GitHubPermissionException,
)
from ..helpers import repository_full_name
from ..models.events import GitHubEventModel
from .base import BaseNamespace

if TYPE_CHECKING:
    from ..client import GitHubClient

_DEFAULT_BACKOFF = 300
_DEFAULT_POLL = 60


class _GitHubEventsBaseNamespace(BaseNamespace):
    """Methods for the events namespace"""

    def __init__(
        self,
        client: GitHubClient,
        space: Literal["users"] | Literal["repos"] | Literal["orgs"],
    ) -> None:
        super().__init__(client)
        self._space = space
        self._subscriptions: Dict[str, asyncio.TimerHandle[None]] = {}

    @staticmethod
    async def _wait(wait_time: float) -> None:
        """Wait for x seconds"""
        await asyncio.sleep(wait_time)

    async def subscribe(
        self,
        name: str,
        event_callback: Callable[[GitHubEventModel], Awaitable[None]],
        *,
        error_callback: Callable[[GitHubException], Awaitable[None]] | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> str:
        """
         Subscribe to an event stream.
         This returns an ID you can use with the unsubscribe method to stop listening for events.

         **Arguments**:

         `name`

         The name to return evets from, example "octocat/hello-world"

         `event_callback`

         An async funtion that will be called when new events come in,
         the event will be passed as the first argument.

         `error_callback` (Optional)

         An async funtion that will be called when errors occour,
         the exception that where raised will be passed.

        https://docs.github.com/en/rest/reference/activity#list-public-events
        """
        subscription_id = str(uuid4())

        async def _subscriber():
            _last_etag: str | None = None
            _poll_time: int = 60
            _target_time = datetime.utcnow().isoformat()
            LOGGER.debug("Starting event subscription for github.com/%s", name)
            while subscription_id in self._subscriptions:
                try:
                    response = await self._client.async_call_api(
                        endpoint=f"/{self._space}/{name}/events",
                        etag=_last_etag,
                        **kwargs,
                    )
                except GitHubNotModifiedException:
                    await self._wait(_poll_time)
                    continue
                except (
                    GitHubAuthenticationException,
                    GitHubNotFoundException,
                    GitHubPermissionException,
                ) as err:
                    await error_callback(err)
                    break
                except GitHubException as err:
                    if error_callback is not None:
                        await error_callback(err)
                    await self._wait(_DEFAULT_BACKOFF)
                    continue
                else:
                    _last_etag = response.headers.etag
                    _poll_time = (
                        int(response.headers.x_poll_interval)
                        if response.headers.x_poll_interval
                        else _DEFAULT_POLL
                    )

                    response.data = [
                        GitHubEventModel(event) for event in reversed(response.data or [])
                    ]

                    for event in response.data:
                        if event.created_at < _target_time:
                            continue
                        _target_time = event.created_at

                        LOGGER.debug("New %s for %s", event.type, name)
                        try:
                            await event_callback(event)
                        except Exception as err:
                            if error_callback is not None:
                                await error_callback(GitHubException(err))

                await self._wait(_poll_time)

            LOGGER.debug("Stopping event subscription for github.com/%s", name)
            self.unsubscribe(subscription_id=subscription_id)

        handler = self._client._loop.call_soon(self._client._loop.create_task, _subscriber())
        self._subscriptions[subscription_id] = handler

        return subscription_id

    def unsubscribe(self, *, subscription_id: str | None = None) -> None:
        """
        Unsubscribe to an event stream

        **Arguments**:

        `subscription_id` (Optional)

        The ID you got when you subscribed, if omitted all active subscriptions will be stopped.
        """
        if not subscription_id:
            for subscription_id in list(self._subscriptions):
                handler = self._subscriptions[subscription_id]
                handler.cancel()
                del self._subscriptions[subscription_id]
            return
        if handler := self._subscriptions.get(subscription_id):
            handler.cancel()
            del self._subscriptions[subscription_id]


class GitHubEventsReposNamespace(_GitHubEventsBaseNamespace):
    """Methods for the repository events namespace"""

    def __init__(self, client: GitHubClient) -> None:
        super().__init__(client, space="repos")

    async def subscribe(
        self,
        repository: RepositoryType,
        event_callback: Callable[[GitHubEventModel], Awaitable[None]],
        *,
        error_callback: Callable[[], Awaitable[None]] | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> str:
        """
         Subscribe to an event stream.
         This returns an ID you can use with the unsubscribe method to stop listening for events.

         **Arguments**:

         `repository`

         The repository to return evets from, example "octocat/hello-world"

         `event_callback`

         An async funtion that will be called when new events come in,
         the event will be passed as the first argument.

         `error_callback` (Optional)

         An async funtion that will be called when errors occour,
         the exception that where raised will be passed.

        https://docs.github.com/en/rest/reference/activity#list-repository-events
        """
        return await super().subscribe(
            name=repository_full_name(repository),
            event_callback=event_callback,
            error_callback=error_callback,
            **kwargs,
        )
