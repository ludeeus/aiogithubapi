"""
AioGitHub: RateLimits

https://developer.github.com/v3/rate_limit/
"""
# pylint: disable=missing-docstring
from datetime import datetime


class RateLimitResources:
    """Ratelimit resources."""

    def __init__(self, rate_data):
        """Initialize."""
        self.rate_data = rate_data
        self.limit = None
        self.remaining = None
        self.reset = None

    @property
    def reset_utc(self):
        """Return date + time in UTC for next reset."""
        if self.reset is None:
            return None
        return datetime.utcfromtimestamp(self.reset)


class AIOGithubRateLimits:
    """Remainding Ratelimits."""

    def __init__(self, attributes):
        """Initialize."""
        self.attributes = attributes
        self.core = RateLimitResources(attributes.get("resources", {}).get("core"))
        self.search = RateLimitResources(attributes.get("resources", {}).get("search"))
        self.graphql = RateLimitResources(
            attributes.get("resources", {}).get("graphql")
        )
        self.integration_manifest = RateLimitResources(
            attributes.get("resources", {}).get("integration_manifest")
        )

    @property
    def limit(self):
        return self.attributes.get("rate", {}).get("limit")

    @property
    def remaining(self):
        return self.attributes.get("rate", {}).get("remaining")

    @property
    def reset(self):
        return self.attributes.get("rate", {}).get("reset")

    @property
    def reset_utc(self):
        """Return date + time in UTC for next reset."""
        if self.reset is None:
            return None
        return datetime.utcfromtimestamp(self.reset)
