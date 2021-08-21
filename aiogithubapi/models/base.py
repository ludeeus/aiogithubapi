"""Base class for all GitHub objects."""
from __future__ import annotations

from logging import Logger
from typing import Any, Dict

from ..const import LOGGER

IGNORE_KEYS = ("node_id", "performed_via_github_app", "_links")


class GitHubBase:
    """Base class for all GitHub objects."""

    logger: Logger = LOGGER

    @staticmethod
    def slugify(value: str) -> str:
        """Slugify."""
        return str(value).replace("-", "_").lower()


class GitHubDataModelBase(GitHubBase):
    """Base class for all GitHub data objects."""

    _raw_data: Any | None = None
    _log_missing: bool = True
    _process_data: bool = True
    _slugify_keys: bool = True

    def __init__(self, data: Dict[str, Any]) -> None:
        """Init."""
        self._raw_data = data
        if self._process_data:
            for key, value in self._raw_data.items():
                if self._slugify_keys:
                    key = self.slugify(key)
                if hasattr(self, key):
                    if handler := getattr(self, f"_generate_{key}", None):
                        value = handler(value)
                    self.__setattr__(key, value)
                elif self._log_missing and key not in IGNORE_KEYS:
                    self.logger.debug(
                        "'%s' is missing key '%s' for %s",
                        self.__class__.__name__,
                        key,
                        type(value),
                    )
        self.__post_init__()

    def __post_init__(self):
        """Post init."""

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Return attributes as a dict."""

        def expand_value_if_needed(value: Any) -> Any:
            if isinstance(value, GitHubDataModelBase):
                return value.as_dict
            if isinstance(value, list):
                return [expand_value_if_needed(v) for v in value]
            return value

        return {
            key: expand_value_if_needed(value)
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }
