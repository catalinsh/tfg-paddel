import pandas as pd
from tsfresh import extract_features


def extract_fresh_features(time_series) -> pd.Series:
    fresh_features = extract_features(
        time_series, column_id="id", n_jobs=1, disable_progressbar=True
    )
    return fresh_features.iloc[0]
