import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from tsfresh.utilities.dataframe_functions import impute

from paddel import settings
from paddel.enums import Gender, Group, Side
from paddel.utilities import contains_letters_in_order


def filter_min_detection_time(
    misc_df: pd.DataFrame, classic_df: pd.DataFrame, fresh_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Filters out instances that don't the minimum detection time needed to be considered.

    Args:
        misc_df (pd.DataFrame): Miscelaneous dataframe.
        classic_df (pd.DataFrame): Classic dataframe.
        fresh_df (pd.DataFrame): TSFresh features dataframe.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Filtered dataframes.
    """

    mask = misc_df["detection_time"] >= settings.min_detection_seconds
    return misc_df[mask], classic_df[mask], fresh_df[mask]


def filter_misc_null_values(
    misc_df: pd.DataFrame, classic_df: pd.DataFrame, fresh_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Filter out columns with null attributes in miscelaneous dataframe

    Args:
        misc_df (pd.DataFrame): Miscelaneous dataframe.
        classic_df (pd.DataFrame): Classic dataframe.
        fresh_df (pd.DataFrame): TSFresh features dataframe.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Filtered dataframes.
    """
    mask = misc_df.notnull().all(axis=1)
    return misc_df[mask], classic_df[mask], fresh_df[mask]


@np.vectorize
def parse_group(group: str) -> int:
    """Parse group to appropiate value.

    Args:
        group (str): Individual group string.

    Returns:
        int: Individual group value.
    """
    if "CONTROL" in group.upper():
        return Group.CONTROL
    elif "ID" in group.upper():
        return Group.ID
    else:
        return np.nan


@np.vectorize
def parse_hand(hand: str) -> int:
    """Parse hand to appropiate value.

    Args:
        hand (str): Hand string.

    Returns:
        int: Hand value.
    """
    if contains_letters_in_order("DERECHA", hand.upper()):
        return Side.RIGHT
    elif contains_letters_in_order("IZQUIERDA", hand.upper()):
        return Side.LEFT
    else:
        return np.nan


@np.vectorize
def parse_gender(gender: str) -> int:
    """Parse gender to appropiate value.

    Args:
        gender (str): Hand string.

    Returns:
        int: Gender value.
    """
    if gender.upper() == "M":
        return Gender.FEMALE
    elif gender.upper() == "H":
        return Gender.MALE
    else:
        return np.nan


@np.vectorize
def parse_age(age: str) -> int:
    """Parse age to appropiate value.

    Args:
        age (str): Hand string.

    Returns:
        int: Age value.
    """
    if age.isnumeric():
        return int(age)
    else:
        return -1


@np.vectorize
def parse_handedness(handedness: str) -> int:
    """Parse handedness to appropriate value.

    Args:
        handedness (str): Handedness string.

    Returns:
        int: Handedness value.
    """
    if handedness.upper() == "D":
        return Side.RIGHT
    elif handedness.upper() == "Z":
        return Side.LEFT
    else:
        return np.nan


def encode_strings(misc_df: pd.DataFrame):
    """Encodes strings into numerical value (enum).

    Args:
        misc_df (pd.DataFrame): Dataframe with attributes to encode.
    """
    misc_df["group"] = parse_group(misc_df["sample_name"])
    misc_df["hand"] = parse_hand(misc_df["hand"])
    misc_df["gender"] = parse_gender(misc_df["gender"])
    misc_df["age"] = parse_age(misc_df["age"])
    misc_df["handedness"] = parse_handedness(misc_df["handedness"])


def drop_unnecessary_columns(
    misc_df: pd.DataFrame, classic_df: pd.DataFrame, fresh_df: pd.DataFrame
):
    """Removes unnecessary or irrelevant columns inplace from given dataframes.

    Args:
        misc_df (pd.DataFrame): Miscelaneous dataframe.
        classic_df (pd.DataFrame): Classic dataframe.
        fresh_df (pd.DataFrame): TSFresh features dataframe.
    """
    misc_df.drop(
        ["sample_name", "date", "video_path", "detection_time", "hand", "handedness"],
        axis=1,
        inplace=True,
    )


def clean(
    misc_df: pd.DataFrame, classic_df: pd.DataFrame, fresh_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Clean dataframes.

    Args:
        misc_df (pd.DataFrame): Miscelaneous dataframe.
        classic_df (pd.DataFrame): Classic dataframe.
        fresh_df (pd.DataFrame): TSFresh features dataframe.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Cleaned dataframes.
    """

    misc_df, classic_df, fresh_df = filter_misc_null_values(
        misc_df, classic_df, fresh_df
    )
    misc_df, classic_df, fresh_df = filter_min_detection_time(
        misc_df, classic_df, fresh_df
    )

    encode_strings(misc_df)

    misc_df, classic_df, fresh_df = filter_misc_null_values(
        misc_df, classic_df, fresh_df
    )

    misc_df["dominant_hand"] = misc_df["hand"] & misc_df["handedness"]

    drop_unnecessary_columns(misc_df, classic_df, fresh_df)

    imp = SimpleImputer(missing_values=-1, strategy="median", copy=False)
    misc_df = pd.DataFrame(imp.fit_transform(misc_df), columns=misc_df.columns)

    impute(fresh_df)

    misc_df.reset_index(inplace=True, drop=True)
    classic_df.reset_index(inplace=True, drop=True)
    fresh_df.reset_index(inplace=True, drop=True)

    return misc_df, classic_df, fresh_df
