"""Custom exceptions for aiogithubapi."""


class GitHubException(BaseException):
    """
    This is raised when unknown exceptions occour.

    And it's used as a base for all other exceptions
    so if you want to catch all GitHub related errors
    you should catch this base exception.
    """


class GitHubConnectionException(GitHubException):
    """This is raised when there is a connection issue with GitHub."""


class GitHubRatelimitException(GitHubException):
    """This is raised when the ratelimit is reached."""


class GitHubNotModifiedException(GitHubException):
    """This is raised when the providede ETag matches and the content has not been modified."""


class GitHubAuthenticationException(GitHubException):
    """This is raised when we recieve an authentication issue."""
