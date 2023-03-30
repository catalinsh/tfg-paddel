from pathlib import Path

import pandas as pd

from paddel.preprocessing.cleaning import clean
from paddel.preprocessing.input.data import get_input_data


def get_data(
    videos_dir: Path, cache_dir: Path = Path()
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series]:
    misc_df, classic_df, fresh_df = get_input_data(videos_dir, cache_dir)
    misc_df, classic_df, fresh_df = clean(misc_df, classic_df, fresh_df)

    return misc_df, classic_df, fresh_df, misc_df.pop("group")
