"""Fixtures."""
# pylint: disable=missing-docstring
import pytest


@pytest.fixture()
def contents_list_response():
    return [
        {
            "type": "file",
            "size": 625,
            "name": "octokit.rb",
            "path": "lib/octokit.rb",
            "sha": "fff6fe3a23bf1c8ea0692b4a883af99bee26fd3b",
            "url": "https://api.github.com/repos/octokit/octokit.rb/contents/lib/octokit.rb",
            "git_url": "https://api.github.com/repos/octokit/octokit.rb/git/blobs/fff6fe3a23bf1c8ea0692b4a883af99bee26fd3b",
            "html_url": "https://github.com/octokit/octokit.rb/blob/main/lib/octokit.rb",
            "download_url": "https://raw.githubusercontent.com/octokit/octokit.rb/main/lib/octokit.rb",
            "_links": {
                "self": "https://api.github.com/repos/octokit/octokit.rb/contents/lib/octokit.rb",
                "git": "https://api.github.com/repos/octokit/octokit.rb/git/blobs/fff6fe3a23bf1c8ea0692b4a883af99bee26fd3b",
                "html": "https://github.com/octokit/octokit.rb/blob/main/lib/octokit.rb",
            },
        },
        {
            "type": "dir",
            "size": 0,
            "name": "octokit",
            "path": "lib/octokit",
            "sha": "a84d88e7554fc1fa21bcbc4efae3c782a70d2b9d",
            "url": "https://api.github.com/repos/octokit/octokit.rb/contents/lib/octokit",
            "git_url": "https://api.github.com/repos/octokit/octokit.rb/git/trees/a84d88e7554fc1fa21bcbc4efae3c782a70d2b9d",
            "html_url": "https://github.com/octokit/octokit.rb/tree/main/lib/octokit",
            "download_url": None,
            "_links": {
                "self": "https://api.github.com/repos/octokit/octokit.rb/contents/lib/octokit",
                "git": "https://api.github.com/repos/octokit/octokit.rb/git/trees/a84d88e7554fc1fa21bcbc4efae3c782a70d2b9d",
                "html": "https://github.com/octokit/octokit.rb/tree/main/lib/octokit",
            },
        },
    ]


@pytest.fixture()
def contents_file_response():
    return {
        "type": "file",
        "encoding": "base64",
        "size": 5362,
        "name": "README.md",
        "path": "README.md",
        "content": "",
        "sha": "3d21ec53a331a6f037a91c368710b99387d012c1",
        "url": "https://api.github.com/repos/octokit/octokit.rb/contents/README.md",
        "git_url": "https://api.github.com/repos/octokit/octokit.rb/git/blobs/3d21ec53a331a6f037a91c368710b99387d012c1",
        "html_url": "https://github.com/octokit/octokit.rb/blob/main/README.md",
        "download_url": "https://raw.githubusercontent.com/octokit/octokit.rb/main/README.md",
        "_links": {
            "git": "https://api.github.com/repos/octokit/octokit.rb/git/blobs/3d21ec53a331a6f037a91c368710b99387d012c1",
            "self": "https://api.github.com/repos/octokit/octokit.rb/contents/README.md",
            "html": "https://github.com/octokit/octokit.rb/blob/main/README.md",
        },
    }
