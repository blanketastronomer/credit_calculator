from pathlib import Path


def text_from_file(file_name: str, stripped: bool = False) -> str:
    """
    Helper for getting text from a file.

    :param file_name: File to grab text from
    :param stripped: Whether or not to strip the last character from the file
    :return: Text of the given file
    """
    test_directory: Path = Path(__file__).parent.parent
    path: Path = test_directory / file_name

    if stripped:
        return path.read_text().strip()
    else:
        return path.read_text()
