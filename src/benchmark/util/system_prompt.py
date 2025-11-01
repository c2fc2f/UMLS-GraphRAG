def system_prompt(base: str, choices: list[str]) -> str:
    """
    Replaces placeholders in the base string with the given choices.

    Parameters:
    - base (str): The template string containing placeholders '{{CHOICES}}'.
    - choices (list[str]): Possible choices for the answer

    Returns:
    - str: The formatted string with placeholders replaced.
    """
    return base.replace("{{CHOICES}}", " or ".join(choices))
