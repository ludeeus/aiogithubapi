# aiogithubapi

[![codecov](https://codecov.io/gh/ludeeus/aiogithubapi/branch/main/graph/badge.svg)](https://codecov.io/gh/ludeeus/aiogithubapi)
![python version](https://img.shields.io/badge/Python-3.8=><=3.10-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/aiogithubapi)](https://pypi.org/project/aiogithubapi)
![Actions](https://github.com/ludeeus/aiogithubapi/workflows/Actions/badge.svg?branch=main)

_Asynchronous Python client for the GitHub API_

This is not a full client for the API (Have you seen it, it's huge), and will probably never be.
Things are added when needed or requested.

If something you need is missing please raise [a fearure request to have it added](https://github.com/ludeeus/aiogithubapi/issues/new?assignees=&labels=enhancement&template=feature_request.md) or [create a PR 🎉](#contribute).
You can also use [`GitHubAPI.generic`](https://aiogithubapi.netlify.app/github.html#aiogithubapi.github.GitHub.generic)
while you wait for your request or contribution to be implemented.

For examples on how to use it see [the documentation](https://aiogithubapi.netlify.app/) and/or the [tests directory](./tests).

## Install

```bash
python3 -m pip install aiogithubapi
```

## Project transition

**Note: This project is currently in a transition phase.**

In august 2021 a new API interface was introduced (in [#42](https://github.com/ludeeus/aiogithubapi/pull/42)). With that addition, all parts of the old interface is now considered deprecated.
Which includes:

- The [`aiogithubapi.common`](./aiogithubapi/common) module
- The [`aiogithubapi.legacy`](./aiogithubapi/legacy) module
- The [`aiogithubapi.objects`](./aiogithubapi/objects) module
- All classes starting with `AIOGitHub`
- The `async_call_api` function in the [`aiogithubapi.helpers.py`](./aiogithubapi/helpers.py) file
- The `GitHubDevice` class in `aiogithubapi`, replaced with `GitHubDeviceAPI`
- The `GitHub` class in `aiogithubapi`, replaced with `GitHubAPI`

Later this year, warning logs will start to be emitted for deprecated code.

Early next year, the old code will be removed.

## Contribute

**All** contributions are welcome!

1. Fork the repository
2. Clone the repository locally and open the devcontainer or use GitHub codespaces
3. Do your changes
4. Lint the files with `make lint`
5. Ensure all tests passes with `make test`
6. Ensure 100% coverage with `make coverage`
7. Commit your work, and push it to GitHub
8. Create a PR against the `main` branch
