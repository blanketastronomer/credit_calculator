from typing import Any


def value_missing(value: Any) -> bool:
    """
    Check if a value is missing.

    :param value: Value to check

    :return: True if None (missing) else False
    """
    return value is None
