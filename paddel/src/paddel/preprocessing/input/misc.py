import re
from pathlib import Path

import pandas as pd


def extract_filename_fields(filename: str) -> dict[str, str]:
    """Extract the different fields from the given filename.

    Args:
        filename (str): Filename.

    Returns:
        dict[str, str]: Dictionary with fields.
    """
    pattern = re.compile(
        r"(?P<sample_name>\w+)"
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
        return {key: None for key in pattern.groupindex}

    return match.groupdict()


def extract_misc_features(path: Path) -> pd.Series:
    """Obtains the filename features from the file in the given path.

    Args:
        path (Path): Path to get features from.

    Returns:
        pd.Series: Dictionary with the parsed features.
    """
    filename = path.stem
    fields = extract_filename_fields(filename)

    ret = pd.Series(fields)
    ret["video_path"] = path

    return ret
