def user_prompt(base: str, intent: str, request: str) -> str:
    """
    Replaces placeholders in the base string with the given intent and
    request.

    Parameters:
    - base (str): The template string containing placeholders '{{INTENT}}' and
        '{{REQUEST}}'.
    - intent (str): The intent to insert into the template.
    - request (str): The specific request to insert into the template.

    Returns:
    - str: The formatted string with placeholders replaced.
    """
    return base.replace("{{INTENT}}", intent).replace("{{REQUEST}}", request)
