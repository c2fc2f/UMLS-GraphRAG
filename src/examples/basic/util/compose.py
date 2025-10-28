from typing import Callable


def compose(*functions: Callable[[str], str]) -> Callable[[str], str]:
    """
    Compose multiple functions into one (left to right execution).

    Parameters:
        *functions: Variable number of functions to compose.

    Returns:
        A new function that applies all functions in sequence.
    """

    def composed(text: str) -> str:
        for func in functions:
            text = func(text)
        return text

    return composed
