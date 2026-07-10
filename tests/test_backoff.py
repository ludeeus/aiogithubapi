"""Test the async_backoff decorator."""

from unittest.mock import AsyncMock, patch

import pytest

from aiogithubapi.backoff import async_backoff


@pytest.mark.asyncio
async def test_returns_on_first_success():
    """Test that a successful call is not retried and does not sleep."""
    calls = 0

    @async_backoff(ValueError, max_tries=5)
    async def call():
        nonlocal calls
        calls += 1
        return "ok"

    with patch("aiogithubapi.backoff.asyncio.sleep", AsyncMock()) as sleep:
        assert await call() == "ok"

    assert calls == 1
    sleep.assert_not_called()


@pytest.mark.asyncio
async def test_retries_then_succeeds():
    """Test that listed exceptions are retried until success."""
    calls = 0

    @async_backoff((ValueError, KeyError), max_tries=5)
    async def call():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise KeyError("boom")
        return "ok"

    with patch("aiogithubapi.backoff.asyncio.sleep", AsyncMock()) as sleep:
        assert await call() == "ok"

    assert calls == 3
    assert sleep.call_count == 2
    for attempt, call_args in enumerate(sleep.call_args_list):
        assert 0 <= call_args.args[0] <= 2**attempt


@pytest.mark.asyncio
async def test_raises_after_max_tries():
    """Test that the exception is re-raised after max_tries attempts."""
    calls = 0

    @async_backoff(ValueError, max_tries=5)
    async def call():
        nonlocal calls
        calls += 1
        raise ValueError("boom")

    with patch("aiogithubapi.backoff.asyncio.sleep", AsyncMock()) as sleep:
        with pytest.raises(ValueError):
            await call()

    assert calls == 5
    assert sleep.call_count == 4


@pytest.mark.asyncio
async def test_unlisted_exception_not_retried():
    """Test that exceptions not in the tuple propagate immediately."""
    calls = 0

    @async_backoff(ValueError, max_tries=5)
    async def call():
        nonlocal calls
        calls += 1
        raise KeyError("boom")

    with patch("aiogithubapi.backoff.asyncio.sleep", AsyncMock()) as sleep:
        with pytest.raises(KeyError):
            await call()

    assert calls == 1
    sleep.assert_not_called()


def test_preserves_metadata():
    """Test that the decorator preserves the wrapped function metadata."""

    @async_backoff(ValueError)
    async def documented_call():
        """Some docstring."""

    assert documented_call.__name__ == "documented_call"
    assert documented_call.__doc__ == "Some docstring."
