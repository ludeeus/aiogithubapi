"""Test const."""

from aiogithubapi.const import StrEnum, IntEnum


def test_enum_value():
    """Test enum value."""

    class TestStrEnum(StrEnum):
        """Test StrEnum class"""

        TEST = "test"

    class TestIntEnum(IntEnum):
        """Test StrEnum class"""

        TEST = 4

    assert TestStrEnum.TEST == "test"
    assert TestStrEnum.TEST.value == "test"
    assert str(TestStrEnum.TEST) == "test"

    assert TestIntEnum.TEST == 4
    assert TestIntEnum.TEST.value == 4
    assert int(TestIntEnum.TEST) == 4
