def read_to_string(path: str) -> str:
    """
    Reads the entire contents of a file and returns it as a string.

    Parameters:
    - path (str): The path to the file to read.

    Returns:
    - str: The contents of the file as a string.
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
