"""AIOGitHubAPI: Exceptions"""
from ..exceptions import (
    GitHubAuthenticationException,
    GitHubException,
    GitHubNotModifiedException,
    GitHubRatelimitException,
)


class AIOGitHubAPIException(GitHubException):
    """
    Raise this when something is off.

    Deprecated: use `aiogithubapi.exceptions.GitHubException` instead
    """


class AIOGitHubAPIRatelimitException(GitHubRatelimitException, AIOGitHubAPIException):
    """
    Raise this when we hit the ratelimit.

    Deprecated: use `aiogithubapi.exceptions.GitHubRatelimitException` instead
    """


class AIOGitHubAPINotModifiedException(GitHubNotModifiedException, AIOGitHubAPIException):
    """
    Raise this when we the content was not modified.

    Deprecated: use `aiogithubapi.exceptions.GitHubNotModifiedException` instead
    """


class AIOGitHubAPIAuthenticationException(GitHubAuthenticationException, AIOGitHubAPIException):
    """
    Raise this when there is an authentication issue.

    Deprecated: use `aiogithubapi.exceptions.GitHubAuthenticationException` instead
    """
