"""Lightweight exponential-backoff retry decorator."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from functools import wraps
import random


def random_float(minimum: float, maximum: float) -> float:
    """Return a random float between minimum and maximum (inclusive)."""
    return random.uniform(minimum, maximum)


def async_backoff[**P, T](
    exceptions: type[BaseException] | tuple[type[BaseException], ...],
    max_tries: int = 5,
    base: float = 2,
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Retry an async function with exponential backoff and full jitter.

    Waits random_float(0, base**attempt) between tries,
    re-raises the last exception after max_tries attempts.
    """

    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            attempt = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions:
                    attempt += 1
                    if attempt >= max_tries:
                        raise
                    await asyncio.sleep(random_float(0, base ** (attempt - 1)))

        return wrapper

    return decorator
