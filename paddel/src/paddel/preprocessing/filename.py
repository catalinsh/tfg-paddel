import re
from pathlib import Path

import numpy as np

from paddel.enums import Gender, Group, Side

FilenameFeatures = np.dtype([("stem", "O"), ("name", "O")])


def extract_filename_fields(filename: str) -> dict[str, str]:
    """Extract the different fields from the given filename.

    :param filename: Filename.
    :return: Dictionary with fields.
    """
    pattern = re.compile(
        r"(?P<group>\w+)"
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
        return {key: "null" for key in pattern.groupindex}

    return match.groupdict()


def parse_group(group: str) -> int:
    """Parse group to appropriate value.

    :param group: Individual type string.
    :return: Individual type value.
    """
    if "CONTROL" in group.upper():
        return Group.CONTROL
    elif "ID" in group.upper():
        return Group.ID
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


def parse_hand(hand: str) -> int:
    """Parse hand to appropriate value.

    :param hand: Hand string.
    :return: Hand value.
    """
    if contains_letters_in_order("DERECHA", hand.upper()):
        return Side.RIGHT
    elif contains_letters_in_order("IZQUIERDA", hand.upper()):
        return Side.LEFT
    else:
        return -1


def parse_gender(gender: str) -> int:
    """Parse gender to appropriate value.

    :param gender: Hand string.
    :return: Gender value.
    """
    if gender.upper() == "M":
        return Gender.FEMALE
    elif gender.upper() == "H":
        return Gender.MALE
    else:
        return -1


def parse_age(age: str) -> int:
    """Parse age to appropriate value.

    :param age: Hand string.
    :return: Age value.
    """
    if age.isnumeric():
        return int(age)
    else:
        return -1


def parse_handedness(handedness: str) -> int:
    """Parse handedness to appropriate value.

    :param handedness: Hand string.
    :return: Handedness value.
    """
    if handedness.upper() == "D":
        return Side.RIGHT
    elif handedness.upper() == "Z":
        return Side.LEFT
    else:
        return -1


def extract_filename_features(path: Path) -> dict[str, int]:
    """Obtains the filename features from the file in the given path.

    :param path: Path to get features from.
    :return: Dictionary with the parsed features.
    """
    filename = path.stem
    fields = extract_filename_fields(filename)

    group = parse_group(fields["group"])
    hand = parse_hand(fields["hand"])
    gender = parse_gender(fields["gender"])
    age = parse_age(fields["age"])
    handedness = parse_handedness(fields["handedness"])

    return {
        "group": group,
        "hand": hand,
        "gender": gender,
        "age": age,
        "handedness": handedness,
    }
