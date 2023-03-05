import numpy as np
import pandas as pd
from tsfresh import extract_features
from tsfresh.feature_extraction.feature_calculators import set_property
from tsfresh.utilities.dataframe_functions import impute

from .dataframes import get_input_data


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def speed(x: pd.Series):
    ix = x.index
    time_seconds = (ix[-1] - ix[0]).total_seconds()

    differences = np.abs(np.diff(x.to_numpy()))

    total_difference = np.sum(differences)

    return total_difference / time_seconds


def clean_data(y, misc_features, classic_features, fresh_features):
    # Drop rows
    indices_to_remove = misc_features.index[misc_features["detection_time"] < 15]

    y.drop(indices_to_remove, inplace=True)
    misc_features.drop(indices_to_remove, inplace=True)
    classic_features.drop(indices_to_remove, inplace=True)
    fresh_features.drop(indices_to_remove, inplace=True)

    # Drop columns
    misc_features.drop(["video_path"], axis=1, inplace=True)

    # Impute
    impute(fresh_features)


def get_data():
    y, misc_features, time_series = get_input_data()

    # Extract classic features
    classic_settings = {speed: None}
    classic_features = extract_features(
        time_series, column_id="id", default_fc_parameters=classic_settings
    )

    # Extract TSFresh default features
    fresh_features = extract_features(time_series, column_id="id")

    return y, misc_features, classic_features, fresh_features
