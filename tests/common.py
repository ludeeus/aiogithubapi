"""Common tests helpers."""
from __future__ import annotations

from dataclasses import dataclass
import json
from logging import Logger
import os
from typing import Any, Dict

from yarl import URL

from aiogithubapi.const import BASE_API_HEADERS, LOGGER, HttpContentType

TEST_LOGGER: Logger = LOGGER

TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CLIENT_ID = "xxxxxx"
DEVICE_CODE = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

TEST_ORGANIZATION = "octocat"
TEST_REPOSITORY_NAME = "octocat/hello-world"
TEST_USER_NAME = "octocat"

EXPECTED_ETAG = 'W/"1234567890abcdefghijklmnopqrstuvwxyz"'


def load_fixture(filename, asjson=False, legacy=True):
    """Load a fixture."""
    filename = f"{filename}.json" if "." not in filename else filename
    path = os.path.join(
        os.path.dirname(__file__),
        "legacy" if legacy else "",
        "fixtures",
        filename.lower().replace("/", "_"),
    )
    TEST_LOGGER.debug("Loading fixture from %s", path)
    with open(path, encoding="utf-8") as fptr:
        if asjson:
            return json.loads(fptr.read())
        return fptr.read()


TEST_REQUEST_HEADERS = {
    **BASE_API_HEADERS,
    "Authorization": f"token {TOKEN}",
}

HEADERS = {**load_fixture("headers.json", asjson=True, legacy=False)}
HEADERS_RATELIMITED = {
    **HEADERS,
    "X-RateLimit-Remaining": "0",
    "X-RateLimit-Used": "5000",
}
HEADERS_TEXT = {**HEADERS, "Content-Type": HttpContentType.TEXT_PLAIN}


TEXT_ENDPOINTS = (
    "markdown",
    "zen",
    "octocat",
    "repos/octocat/hello-world/readme/",
    "repos/octocat/hello-world/readme/test",
)
BYTES_ENDPOINT = ("tarball", "zipball")


@dataclass
class MockResponse:
    """Mock response class."""

    _count = 0

    throw_on_file_error = False

    mock_data: Any | None = None
    mock_data_list: list[Any] | None = None
    mock_endpoint: str = ""
    mock_headers: Dict[str, str] | None = None
    mock_raises: BaseException | None = None
    mock_status: int = 200

    @property
    def status(self):
        """status."""
        return self.mock_status

    @property
    def headers(self):
        """headers."""
        return self.mock_headers or HEADERS

    @property
    def links(self):
        """headers."""
        pages: Dict[str, dict] = {}
        if not self.headers.get("Link"):
            return pages
        for pageentry in self.headers["Link"].split(", "):
            link = URL(pageentry.split(";")[0].replace("<", "").replace(">", ""))
            rel_type = pageentry.split(";")[1].split("=")[1].replace('"', "")
            pages[rel_type] = {"rel": rel_type, "url": link}
        return pages

    async def json(self, **_):
        """json."""
        if self.mock_raises is not None:
            raise self.mock_raises  # pylint: disable=raising-bad-type
        if self.mock_data_list:
            data = self.mock_data_list[self._count]
            self._count += 1
            return data
        if self.mock_data is not None:
            return self.mock_data
        try:
            return load_fixture(self.mock_endpoint, asjson=True, legacy=False)
        except OSError:
            if self.throw_on_file_error:
                raise OSError(f"Missing fixture for {self.mock_endpoint}") from None
            return {}

    async def text(self, **_):
        """text."""
        if self.mock_raises is not None:
            raise self.mock_raises  # pylint: disable=raising-bad-type
        if self.mock_data_list:
            data = self.mock_data_list[self._count]
            self._count += 1
            return json.dumps(data)
        if self.mock_data is not None:
            return json.dumps(self.mock_data)
        try:
            file = (
                self.mock_endpoint
                if self.mock_endpoint not in TEXT_ENDPOINTS
                else f"{self.mock_endpoint}.txt"
            )
            return load_fixture(file, legacy=False)
        except OSError:
            if self.throw_on_file_error:
                raise OSError(f"Missing fixture for {self.mock_endpoint}") from None
            return ""

    async def read(self, **_):
        """read."""
        return b""

    def clear(self):
        """clear."""
        self.mock_data = None
        self.mock_endpoint = ""
        self.mock_headers = None
        self.mock_raises = None
        self.mock_status = 200


class MockedRequests:
    """Mock request class."""

    _calls = []

    def add(self, url: str):
        """add."""
        self._calls.append(url)

    def clear(self):
        """clear."""
        self._calls.clear()

    def __repr__(self) -> str:
        return f"<MockedRequests: {self._calls}>"

    @property
    def called(self) -> int:
        """count."""
        return len(self._calls)

    def has(self, string: str) -> bool:
        """has."""
        return bool([entry for entry in self._calls if string in entry])

    @property
    def last_request(self) -> MockResponse:
        """last url."""
        return self._calls[-1]
