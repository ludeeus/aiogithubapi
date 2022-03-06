"""GitHub reaction data class."""
from pydantic import BaseModel, root_validator


class GitHubReactionModel(BaseModel):
    """GitHub reaction data class."""

    url: str
    total_count: int
    thumbs_up: int
    thumbs_down: int
    laugh: int
    hooray: int
    confused: int
    heart: int
    rocket: int
    eyes: int

    @root_validator(pre=True)
    def _handle_thumps_up_down(cls, values):
        values["thumbs_down"] = values.get("-1", 0)
        values["thumbs_up"] = values.get("+1", 0)
        del values["+1"]
        del values["-1"]
        return values
