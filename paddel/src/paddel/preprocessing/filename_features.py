import logging
import re
from typing import Any, Optional

from paddel.enums import Gender, IndividualType, Side

log = logging.getLogger(__name__)


def extract_filename_fields(filename: str) -> Optional[dict[str, str]]:
    """Match filename to the expected regex pattern and get the fields.

    :param filename: String to match.
    :return: Filename fields or None.
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
        return None

    return match.groupdict()


def contains_letters_in_order(word: str, letters: str) -> bool:
    """Check if the given word contains the given letter in order.

    :param word: Word to check.
    :param letters: Letters to check.
    :return: If the word contains the letters in order.
    """
    regex = ".*".join(letters)
    return re.search(regex, word) is not None


def parse_features(unparsed_features: dict[str, str]) -> Optional[dict[str, Any]]:
    """Parse previously matched features to the adequate feature values.

    :param unparsed_features: Features to parse.
    :return: Parsed features or None.
    """
    features: dict[str, Any] = {}

    individual_type = unparsed_features["individual_type"]
    if "CONTROL" in individual_type.upper():
        features["individual_type"] = IndividualType.CONTROL
    elif "ID" in individual_type.upper():
        features["individual_type"] = IndividualType.ID
    else:
        log.warning("Could not parse individual type of video")
        return None

    hand = unparsed_features["hand"]
    if contains_letters_in_order("DERECHA", hand.upper()):
        features["hand"] = Side.RIGHT
    elif contains_letters_in_order("IZQUIERDA", hand.upper()):
        features["hand"] = Side.LEFT
    else:
        log.warning("Could not parse hand of video")
        return None

    gender = unparsed_features["gender"]
    if gender.upper() == "M":
        features["gender"] = Gender.FEMALE
    elif gender.upper() == "H":
        features["gender"] = Gender.MALE
    else:
        log.warning("Could not parse gender of video")
        return None

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
        log.warning("Could not parse handedness of video")
        return None

    return features


def extract_filename_features(filename: str) -> Optional[dict[str, Any]]:
    """Get features from the given filename.

    :param filename: Filename to get features from.
    :return: Filename features or None.
    """
    features = extract_filename_fields(filename)
    if not features:
        log.warning(f"Could not match filename of {filename}")
        return None

    parsed_features = parse_features(features)
    if not parsed_features:
        log.warning(f"Could not parse features from filename of {filename}")
        return None

    return parsed_features
