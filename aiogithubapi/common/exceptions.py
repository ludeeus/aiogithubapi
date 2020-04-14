"""AIOGitHubAPI: Exceptions"""


class AIOGitHubAPIException(BaseException):
    """Raise this when something is off."""


class AIOGitHubAPIRatelimitException(AIOGitHubAPIException):
    """Raise this when we hit the ratelimit."""


class AIOGitHubAPIAuthenticationException(AIOGitHubAPIException):
    """Raise this when there is an authentication issue."""
