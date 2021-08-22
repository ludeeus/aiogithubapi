"""Test repository dataclass."""
from aiogithubapi import Repository
from aiogithubapi.helpers import repository_full_name


def test_repository():
    """Test repository dataclass."""
    assert (
        repository_full_name(Repository(owner="octocat", repo="Hello-World"))
        == "octocat/Hello-World"
    )
    assert repository_full_name("octocat/Hello-World") == "octocat/Hello-World"
    assert (
        repository_full_name({"owner": "octocat", "repo": "Hello-World"}) == "octocat/Hello-World"
    )
