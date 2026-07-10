"""Lightweight exponential-backoff retry decorator."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from functools import wraps

from .const import LOGGER
from .utils import random_float


def async_backoff[**P, T](
    exceptions: type[BaseException] | tuple[type[BaseException], ...],
    max_tries: int = 5,
    base: float = 2,
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Retry an async function with exponential backoff and full jitter.

    Before retry number n (starting at 1) this waits
    random_float(0, base ** (n - 1)) seconds, and re-raises
    the last exception after max_tries attempts.
    """

    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            attempt = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions as exception:
                    attempt += 1
                    if attempt >= max_tries:
                        raise
                    sleep_seconds = random_float(0, base ** (attempt - 1))
                    LOGGER.debug(
                        "Retrying %s in %.2f seconds (attempt %s of %s) after %r",
                        func.__name__,
                        sleep_seconds,
                        attempt,
                        max_tries,
                        exception,
                    )
                    await asyncio.sleep(sleep_seconds)

        return wrapper

    return decorator
