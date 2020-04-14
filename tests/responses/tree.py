"""Fixtures."""
# pylint: disable=missing-docstring
import pytest


@pytest.fixture()
def tree_response():
    return {
        "sha": "fc6274d15fa3ae2ab983129fb037999f264ba9a7",
        "url": "https://api.github.com/repos/octocat/Hello-World/trees/fc6274d15fa3ae2ab983129fb037999f264ba9a7",
        "tree": [
            {
                "path": "subdir/file.txt",
                "mode": "100644",
                "type": "blob",
                "size": 132,
                "sha": "7c258a9869f33c1e1e1f74fbb32f07c86cb5a75b",
                "url": "https://api.github.com/repos/octocat/Hello-World/git/7c258a9869f33c1e1e1f74fbb32f07c86cb5a75b",
            },
            {
                "path": "subdir",
                "mode": "100644",
                "type": "tree",
                "size": 132,
                "sha": "7c258a9869f33c1e1e1f74fbb32f07c86cb5a75b",
                "url": "https://api.github.com/repos/octocat/Hello-World/git/7c258a9869f33c1e1e1f74fbb32f07c86cb5a75b",
            },
        ],
        "truncated": False,
    }
