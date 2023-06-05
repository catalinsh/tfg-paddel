from pathlib import Path

import pandas as pd

from paddel.preprocessing.cleaning import clean
from paddel.preprocessing.input.data import get_input_data


def get_data(
    videos_dir: Path, cache_dir: Path = None
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series]:
    """Obtains the data to train the models.

    Args:
        videos_dir (Path): Directory where the videos are located.
        cache_dir (Path, optional): Directory to save extracted data for following runs.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series]: Extracted data.
    """
    misc_df, classic_df, fresh_df = get_input_data(videos_dir, cache_dir)
    misc_df, classic_df, fresh_df = clean(misc_df, classic_df, fresh_df)

    return misc_df, classic_df, fresh_df, misc_df.pop("group")
