"""Test repository dataclass."""
from io import BytesIO
import json
from unittest.mock import patch
from aiogithubapi import Repository
from aiogithubapi.helpers import random_float, repository_full_name


def test_random_float():
    """Test random_float returns a float within the given bounds."""
    for _ in range(100):
        value = random_float(0.5, 5)
        assert isinstance(value, float)
        assert 0.5 <= value <= 5


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
