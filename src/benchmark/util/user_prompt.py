def user_prompt(base: str, intent: str, request: str, choices: dict[str, str]) -> str:
    """
    Replaces placeholders in the base string with the given intent and
    request.

    Parameters:
    - base (str): The template string containing placeholders '{{INTENT}}',
        '{{REQUEST}}' and '{{CHOICES}}'.
    - intent (str): The intent to insert into the template.
    - request (str): The specific request to insert into the template.
    - choices (dict[str, str]): Possible choices for the answer

    Returns:
    - str: The formatted string with placeholders replaced.
    """
    return (
        base.replace("{{INTENT}}", intent)
        .replace("{{REQUEST}}", request)
        .replace(
            "{{CHOICES}}",
            "\n".join(f"{key}: {value}" for key, value in choices.items()),
        )
    )
