import re

import pandas as pd

from paddel.enums import Gender, IndividualType, Side


def extract_filename_features(filename: str) -> pd.Series:
    """Extract the different fields from the given filename.

    :param filename: Filename.
    :return: Pandas Series of the features.
    """
    pattern = re.compile(
        r"(?P<individual_type>\w+)"
        r"_"
        r"(?P<date>\d{2}-\d{2}-\d{4})"
        r"_"
        r"(?P<hand>\w+)"
        r" "
        r"\("
        r"(?P<gender>\w)"
        r"-"
        r"(?P<age>\w+)"
        r"-"
        r"(?P<handedness>\w)"
        r"\)"
    )

    match = pattern.match(filename)

    if not match:
        return pd.Series(index=list(pattern.groupindex), dtype=str)

    fields_dict = match.groupdict()
    fields_series = pd.Series(fields_dict, dtype=str)

    return fields_series


def substitute_individual_type(individual_type: str) -> int:
    """Parse individual type to apropiate value.

    :param individual_type: Individual type string.
    :return: Individual type value.
    """
    if "CONTROL" in individual_type.upper():
        return IndividualType.CONTROL
    elif "ID" in individual_type.upper():
        return IndividualType.ID
    else:
        return -1


def contains_letters_in_order(word: str, letters: str) -> bool:
    """Check if the given word contains the given letter in order.

    :param word: Word to check.
    :param letters: Letters to check.
    :return: If the word contains the letters in order.
    """
    regex = ".*".join(letters)
    return re.search(regex, word) is not None


def substitute_hand(hand: str) -> int:
    """Parse hand to apropiate value.

    :param hand: Hand string.
    :return: Hand value.
    """
    if contains_letters_in_order("DERECHA", hand.upper()):
        return Side.RIGHT
    elif contains_letters_in_order("IZQUIERDA", hand.upper()):
        return Side.LEFT
    else:
        return -1


def substitute_gender(gender: str) -> int:
    """Parse gender to apropiate value.

    :param gender: Hand string.
    :return: Gender value.
    """
    if gender.upper() == "M":
        return Gender.FEMALE
    elif gender.upper() == "H":
        return Gender.MALE
    else:
        return -1


def substitute_age(age: str) -> int:
    """Parse age to apropiate value.

    :param age: Hand string.
    :return: Age value.
    """
    if age.isnumeric():
        return int(age)
    else:
        return -1


def substitute_handedness(handedness: str) -> int:
    """Parse handedness to apropiate value.

    :param handedness: Hand string.
    :return: Handedness value.
    """
    if handedness.upper() == "D":
        return Side.RIGHT
    elif handedness.upper() == "Z":
        return Side.LEFT
    else:
        return -1
