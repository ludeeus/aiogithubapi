"""Test the async_backoff decorator."""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from aiogithubapi.backoff import async_backoff


@pytest.mark.asyncio
async def test_returns_on_first_success(caplog: pytest.CaptureFixture):
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
    assert "Retrying" not in caplog.text


@pytest.mark.asyncio
async def test_retries_then_succeeds(caplog: pytest.CaptureFixture):
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

    retry_logs = [message for message in caplog.messages if message.startswith("Retrying call in")]
    assert len(retry_logs) == 2
    assert "(attempt 1 of 5) after KeyError('boom')" in retry_logs[0]
    assert "(attempt 2 of 5) after KeyError('boom')" in retry_logs[1]


@pytest.mark.asyncio
async def test_raises_after_max_tries(caplog: pytest.CaptureFixture):
    """Test that the exception is re-raised after max_tries attempts."""
    calls = 0

    @async_backoff(ValueError, max_tries=5)
    async def call():
        nonlocal calls
        calls += 1
        raise ValueError("boom")

    with patch("aiogithubapi.backoff.asyncio.sleep", AsyncMock()) as sleep:
        with pytest.raises(ValueError, match="boom"):
            await call()

    assert calls == 5
    assert sleep.call_count == 4

    retry_logs = [message for message in caplog.messages if message.startswith("Retrying call in")]
    assert len(retry_logs) == 4
    for retry, message in enumerate(retry_logs, start=1):
        assert f"(attempt {retry} of 5) after ValueError('boom')" in message


@pytest.mark.asyncio
async def test_unlisted_exception_not_retried(caplog: pytest.CaptureFixture):
    """Test that exceptions not in the tuple propagate immediately."""
    calls = 0

    @async_backoff(ValueError, max_tries=5)
    async def call():
        nonlocal calls
        calls += 1
        raise KeyError("boom")

    with patch("aiogithubapi.backoff.asyncio.sleep", AsyncMock()) as sleep:
        with pytest.raises(KeyError, match="boom"):
            await call()

    assert calls == 1
    sleep.assert_not_called()
    assert "Retrying" not in caplog.text


@pytest.mark.asyncio
async def test_cancellation_not_retried(caplog: pytest.CaptureFixture):
    """Test that asyncio.CancelledError propagates even when listed."""
    calls = 0

    @async_backoff((ValueError, asyncio.CancelledError), max_tries=5)
    async def call():
        nonlocal calls
        calls += 1
        raise asyncio.CancelledError

    with patch("aiogithubapi.backoff.asyncio.sleep", AsyncMock()) as sleep:
        with pytest.raises(asyncio.CancelledError):
            await call()

    assert calls == 1
    sleep.assert_not_called()
    assert "Retrying" not in caplog.text


def test_preserves_metadata():
    """Test that the decorator preserves the wrapped function metadata."""

    @async_backoff(ValueError)
    async def documented_call():
        """Some docstring."""

    assert documented_call.__name__ == "documented_call"
    assert documented_call.__doc__ == "Some docstring."
