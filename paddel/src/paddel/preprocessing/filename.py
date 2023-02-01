import re
from typing import Any

from paddel.enums import Gender, IndividualType, Side
from paddel.exceptions import InvalidFilenameError


def extract_filename_fields(filename: str) -> dict[str, str]:
    """Match filename to the expected regex pattern and get the fields.

    :param filename: String to match.
    :return: Filename fields or None.
    :raises InvalidFilenameError: If filename does not match.
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
        raise InvalidFilenameError(f"Filename does not match expected format.")

    return match.groupdict()


def contains_letters_in_order(word: str, letters: str) -> bool:
    """Check if the given word contains the given letter in order.

    :param word: Word to check.
    :param letters: Letters to check.
    :return: If the word contains the letters in order.
    """
    regex = ".*".join(letters)
    return re.search(regex, word) is not None


def parse_features(unparsed_features: dict[str, str]) -> dict[str, Any]:
    """Parse previously matched features to the adequate feature values.

    :param unparsed_features: Features to parse.
    :return: Parsed features or None.
    :raises InvalidFilenameError: If there is a bad field.
    """
    features: dict[str, Any] = {}

    individual_type = unparsed_features["individual_type"]
    if "CONTROL" in individual_type.upper():
        features["individual_type"] = IndividualType.CONTROL
    elif "ID" in individual_type.upper():
        features["individual_type"] = IndividualType.ID
    else:
        raise InvalidFilenameError("Could not parse individual type of video")

    hand = unparsed_features["hand"]
    if contains_letters_in_order("DERECHA", hand.upper()):
        features["hand"] = Side.RIGHT
    elif contains_letters_in_order("IZQUIERDA", hand.upper()):
        features["hand"] = Side.LEFT
    else:
        raise InvalidFilenameError("Could not parse hand of video")

    gender = unparsed_features["gender"]
    if gender.upper() == "M":
        features["gender"] = Gender.FEMALE
    elif gender.upper() == "H":
        features["gender"] = Gender.MALE
    else:
        raise InvalidFilenameError("Could not parse gender of video")

    age = unparsed_features["age"]
    if age.isnumeric():
        features["age"] = int(age)
    else:
        features["age"] = -1

    handedness = unparsed_features["handedness"]
    if handedness.upper() == "D":
        features["handedness"] = Side.RIGHT
    elif handedness.upper() == "Z":
        features["handedness"] = Side.LEFT
    else:
        raise InvalidFilenameError("Could not parse handedness of video")

    return features


def extract_filename_features(filename: str) -> dict[str, Any]:
    """Get features from the given filename.

    :param filename: Filename to get features from.
    :return: Filename features.
    :raises InvalidFilenameError: If filename is invalid.
    """
    try:
        features = extract_filename_fields(filename)
        parsed_features = parse_features(features)
    except InvalidFilenameError as e:
        raise InvalidFilenameError(f"{filename} could not be parsed.") from e

    return parsed_features
