# AIOGitHubAPI

[![codecov](https://codecov.io/gh/ludeeus/aiogithubapi/branch/master/graph/badge.svg)](https://codecov.io/gh/ludeeus/aiogithubapi)

_Asynchronous Python client for the GitHub API_

This is not a full client for the API (Have you seen it, it's huge), and will probably never be.
Things are added when needed.

For examples on how to use it see [the documentation](https://aiogithubapi.netlify.app/) and/or the tests dir.

## Install

```bash
python3 -m pip install -U aiogithubapi
```

## Add Data Objects

_Currently this will only work properly on single GET responses, if the sample response is a list, just use the first dict in the list_

1. Find the response you want from <https://docs.github.com/en/rest/reference>
1. Find the URL directly to the correct section (like <https://docs.github.com/en/rest/reference/issues#get-a-label>)
1. Expand the "Default response" section, and copy the contents to `generate/input.json`
1. Run `python generate/genreate.py && black .`
   1. You will be asked for the URL, laste the link you found in step 2.
   1. You will be asked for the main class name, use something that make sense.

Examples:

- `issues#get-a-label` Would be `IssuesLabel`
- `projects#get-a-project-card` Would be `ProjectCard`
- `pulls#get-a-pull-request` Would be `PullRequest`
- `repos#get-a-branch` Would be `ReposBranch`