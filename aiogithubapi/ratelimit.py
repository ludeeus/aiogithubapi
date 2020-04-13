"""
AioGitHub: RateLimits

https://developer.github.com/v3/rate_limit/
"""
# pylint: disable=missing-docstring
from datetime import datetime


class RateLimitResources:
    """Ratelimit resources."""

    def __init__(self):
        """Initialize."""
        self.limit = None
        self.remaining = None
        self.reset = None

    @property
    def reset_utc(self):
        """Return date + time in UTC for next reset."""
        if self.reset is None:
            return None
        return datetime.utcfromtimestamp(self.reset)

    def load_from_response_headers(self, headers):
        """Load from response headers."""
        self.limit = headers.get("X-RateLimit-Limit", 0)
        self.remaining = headers.get("X-RateLimit-Remaining", 0)
        self.reset = int(headers.get("X-RateLimit-Reset", 0))

    def load_from_response_json(self, data):
        """Load from response headers."""
        self.limit = data.get("limit", 0)
        self.remaining = data.get("remaining", 0)
        self.reset = data.get("reset", 0)


class AIOGithubRateLimits:
    """Remainding Ratelimits."""

    def __init__(self, attributes):
        """Initialize."""
        self.attributes = attributes
        resources = attributes.get("resources", {})

        self.core = RateLimitResources()
        self.core.load_from_response_json(resources.get("core"))

        self.search = RateLimitResources()
        self.search.load_from_response_json(resources.get("search"))

        self.graphql = RateLimitResources()
        self.graphql.load_from_response_json(resources.get("graphql"))

        self.integration_manifest = RateLimitResources()
        self.integration_manifest.load_from_response_json(
            resources.get("integration_manifest")
        )

    @property
    def limit(self):
        return self.core.limit

    @property
    def remaining(self):
        return self.core.remaining

    @property
    def reset(self):
        return self.core.reset

    @property
    def reset_utc(self):
        return self.core.reset_utc

    @property
    def is_ratelimited(self):
        return self.core.remaining == 0
