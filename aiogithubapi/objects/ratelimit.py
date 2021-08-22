"""
AIOGitHubAPI: objects.ratelimit

https://developer.github.com/v3/rate_limit/
"""
# pylint: disable=missing-docstring
from datetime import datetime

from .base import AIOGitHubAPIBase


class AIOGitHubAPIRateLimit(AIOGitHubAPIBase):
    """
    AIOGitHubAPIRateLimit

    Holds information about the current reatelimit status.
    """

    def __init__(self) -> None:
        """Initialize."""
        self.limit = None
        self.remaining = None
        self.reset = None

    @property
    def reset_utc(self) -> None:
        """Return date + time in UTC for next reset."""
        if self.reset is None:
            return None
        return datetime.utcfromtimestamp(int(self.reset))

    def load_from_response_headers(self, headers: dict) -> None:
        """
        Load from response headers.

        :param headers:     A dctionary with the returned headers
        """
        self.limit = headers.get("X-RateLimit-Limit", "0")
        self.remaining = headers.get("X-RateLimit-Remaining", "0")
        self.reset = headers.get("X-RateLimit-Reset", "0")
