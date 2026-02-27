# aiogithubapi

[![codecov](https://codecov.io/gh/ludeeus/aiogithubapi/branch/main/graph/badge.svg)](https://codecov.io/gh/ludeeus/aiogithubapi)
[![PyPI](https://img.shields.io/pypi/v/aiogithubapi)](https://pypi.org/project/aiogithubapi)
![Actions](https://github.com/ludeeus/aiogithubapi/workflows/Actions/badge.svg?branch=main)

_Asynchronous Python client for the GitHub API_

This is not a full client for the API (Have you seen it, it's huge), and will probably never be.
Things are added when needed or requested.

If something you need is missing please raise [a feature request to have it added](https://github.com/ludeeus/aiogithubapi/issues/new?assignees=&labels=enhancement&template=feature_request.md) or [create a PR 🎉](#contribute).

For examples on how to use it see the [tests directory](./tests).

## Install

```bash
python3 -m pip install aiogithubapi
```

## Project transition

**Note: This project is currently in a transition phase.**

In August 2021 a new API interface was introduced (in [#42](https://github.com/ludeeus/aiogithubapi/pull/42)). With that addition, all parts of the old interface are now considered deprecated.
Which includes:

- The [`aiogithubapi.common`](./aiogithubapi/common) module
- The [`aiogithubapi.legacy`](./aiogithubapi/legacy) module
- The [`aiogithubapi.objects`](./aiogithubapi/objects) module
- All classes starting with `AIOGitHub`
- The `async_call_api` function in the [`aiogithubapi/helpers.py`](./aiogithubapi/helpers.py) file
- The `GitHubDevice` class in `aiogithubapi`, replaced with `GitHubDeviceAPI`
- The `GitHub` class in `aiogithubapi`, replaced with `GitHubAPI`

**Warning:** The deprecated code will be removed in a future release. Please migrate to the new API interface.

## Contribute

**All** contributions are welcome!

1. Fork the repository
2. Clone the repository locally and open the devcontainer or use GitHub codespaces
3. Do your changes
4. Lint the files with `scripts/lint`
5. Ensure all tests pass with `scripts/test`
6. Ensure 100% coverage with `scripts/coverage`
7. Commit your work, and push it to GitHub
8. Create a PR against the `main` branch

## Versioning

This project follows [Semantic Versioning](https://semver.org/).

Early releases used semver (`0.1.0`–`2.0.0`), followed by a period of calendar versioning (`21.1.0`–`25.5.0`). Starting with `26.0.0`, the project returns to semver — using `26.x.x` as the starting point to stay above the last calver release and avoid confusing package managers.

Version bumps are determined automatically by PR labels:

- `breaking-change` → **major**
- `feature` / `enhancement` → **minor**
- All other changes → **patch**

## Release

Releases are automated via GitHub Actions. The flow works as follows:

1. PRs are merged to `main` with appropriate labels
2. On every merge, [release-drafter](https://github.com/release-drafter/release-drafter) automatically maintains a **draft GitHub Release** with categorized changelog entries built from PR titles and authors
3. Changelog entries are grouped into: Breaking changes, New features, Enhancements, Bug fixes, Maintenance, Documentation, and Dependencies
4. A maintainer reviews the draft and **publishes** the release via the GitHub Releases UI
5. Publishing creates a git tag and triggers the release workflow, which stamps the version into `pyproject.toml`, builds the package, and publishes it to [PyPI](https://pypi.org/project/aiogithubapi) via OIDC trusted publishing
