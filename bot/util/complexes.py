import json


def get_complexes() -> dict:
    """Reads and returns the file located at ../complexes.json as a Python
    dictionary. This file contains aliases from both complex names and
    abbreviations into a common name so that the user can execute `!staff TJ`
    or `!staff Thomas Jefferson`, for instance.
    """
    with open("complexes.json", "r") as complexes_file:
        return json.loads(complexes_file.read())


complexes = get_complexes()


def get_complex_name(abbr: str):
    """Returns the full complex name, given either the full name or
    abbreviation. Returns None if the complex does not exist.

    Arguments:
    abbr -- the full name or abbreviation of the complex
    """
    return complexes.get(abbr)
