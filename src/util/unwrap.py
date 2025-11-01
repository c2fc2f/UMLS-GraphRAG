def unwrap(value: str | None) -> str:
    """
    Returns the given string if it is not None, otherwise raises a ValueError.

    Parameters:
    - value (str | None): The string to unwrap.

    Returns:
    - str: The unwrapped string if it is not None.

    Raises:
    - ValueError: If the value is None.
    """
    if value is None:
        raise ValueError("called `unwrap()` on a `None` value")
    return value
