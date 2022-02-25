"""
Methods for the events namespace

https://docs.github.com/en/rest/reference/activity#events
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, List, Literal
from uuid import UUID, uuid4

from ..const import LOGGER, GitHubRequestKwarg, RepositoryType
from ..exceptions import (
    GitHubAuthenticationException,
    GitHubException,
    GitHubNotModifiedException,
)
from ..models.events import GitHubEventModel
from .base import BaseNamespace

if TYPE_CHECKING:
    from ..client import GitHubClient


class _GitHubEventsBaseNamespace(BaseNamespace):
    """Methods for the events namespace"""

    def __init__(
        self,
        client: GitHubClient,
        space: Literal["users"] | Literal["repos"] | Literal["orgs"],
    ) -> None:
        super().__init__(client)
        self._space = space
        self._subscriptions: List[UUID] = []

    async def subscribe(
        self,
        name: str,
        event_callback: Callable[[GitHubEventModel], Awaitable[None]],
        *,
        error_callback: Callable[[GitHubException], Awaitable[None]] | None = None,
        **kwargs: Dict[GitHubRequestKwarg, Any],
    ) -> UUID:
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
        uuid = uuid4()
        self._subscriptions.append(uuid)

        async def _subscriber():
            _last_etag: str | None = None
            _backoff_time: int = 300
            _poll_time: int = 60
            _start_time = datetime.utcnow()
            LOGGER.debug("Starting activity stream for github.com/%s", name)
            while uuid in self._subscriptions:
                try:
                    response = await self._client.async_call_api(
                        endpoint=f"/{self._space}/{name}/events",
                        etag=_last_etag,
                        **kwargs,
                    )
                except GitHubNotModifiedException:
                    await asyncio.sleep(_poll_time)
                    continue
                except GitHubAuthenticationException as err:
                    await error_callback(err)
                    break
                except GitHubException as err:
                    if error_callback is not None:
                        await error_callback(err)
                    await asyncio.sleep(_backoff_time)
                    continue
                else:
                    _last_etag = response.headers.etag
                    _poll_time = int(response.headers.x_poll_interval or 60)

                response.data = [GitHubEventModel(event) for event in response.data or []]

                if response.data:
                    for event in response.data:
                        if event.created_at < _start_time.isoformat():
                            continue

                        LOGGER.debug("New %s for %s", event.type, event)
                        try:
                            await event_callback(event)
                        except Exception as err:
                            if error_callback is not None:
                                await error_callback(GitHubException(err))

                await asyncio.sleep(_poll_time)

            if uuid in self._subscriptions:
                self._subscriptions.pop(uuid)

        self._client._loop.call_later(1, self._client._loop.create_task, _subscriber())

        return uuid

    def unsubscribe(self, *, subscription: str | None = None) -> None:
        """
        Unsubscribe to an event stream

        **Arguments**:

        `subscription` (Optional)

        The ID you got when you subscribed, if omitted all active subscriptions will be stopped.
        """
        if not subscription:
            self._subscriptions.clear()
            return
        if subscription in self._subscriptions:
            self._subscriptions.pop(subscription)


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
    ) -> UUID:
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
            name=repository,
            event_callback=event_callback,
            error_callback=error_callback,
            **kwargs,
        )
