"""Utils for AIOGitHubAPI."""

from __future__ import annotations

import random


def random_float(minimum: float, maximum: float) -> float:
    """Return a random float between minimum and maximum (inclusive)."""
    return random.uniform(minimum, maximum)
