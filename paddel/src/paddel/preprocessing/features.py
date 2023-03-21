import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from tsfresh import extract_features
from tsfresh.feature_extraction.feature_calculators import set_property
from tsfresh.utilities.dataframe_functions import impute

from .. import settings
from .datagetter import DataGetter


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def mean_speed(x: pd.Series):
    time = x.index
    time_seconds = (time[-1] - time[0]).total_seconds()

    differences = np.abs(np.diff(x.to_numpy()))

    total_difference = np.sum(differences)

    return total_difference / time_seconds


def rolling_std_prominence_maximums(x: pd.Series):
    window = pd.to_timedelta(settings.rolling_std_seconds, unit="seconds")
    rolling_std = x.rolling(window, center=True).std().to_numpy()

    maximums, _ = find_peaks(
        x.to_numpy(),
        prominence=rolling_std * 2,
    )
    return x.iloc[maximums].index


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def frequency_of_maximums(x: pd.Series):
    time = x.index
    maximums = rolling_std_prominence_maximums(x)
    time_seconds = (time[-1] - time[0]).total_seconds()

    return len(maximums) / time_seconds


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def frequency_of_minimums(x: pd.Series):
    return frequency_of_maximums(-x)


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def average_of_maximums(x: pd.Series):
    maximums_idx = rolling_std_prominence_maximums(x)
    maximums = x[maximums_idx]
    return np.mean(maximums)


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def std_of_maximums(x: pd.Series):
    maximums_idx = rolling_std_prominence_maximums(x)
    maximums = x[maximums_idx]
    return np.std(maximums)


def get_slots(x: pd.Series):
    slot_size = pd.to_timedelta(settings.slot_size_seconds, unit="seconds")
    start_slot_mark = x.index[0] + slot_size
    end_slot_mark = x.index[-1] - slot_size

    start_slot = x[:start_slot_mark]
    end_slot = x[end_slot_mark:]

    return start_slot, end_slot


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def slotted_difference_of_frequency_of_minimums(x: pd.Series):
    start_slot, end_slot = get_slots(x)
    return frequency_of_minimums(start_slot) - frequency_of_minimums(end_slot)


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def slotted_difference_of_average_of_maximums(x: pd.Series):
    start_slot, end_slot = get_slots(x)
    return average_of_maximums(start_slot) - average_of_maximums(end_slot)


def clean_data(y, misc_features, classic_features, fresh_features):
    # Drop rows
    indices_to_remove = misc_features.index[misc_features["detection_time"] < 15]

    y.drop(indices_to_remove, inplace=True)
    misc_features.drop(indices_to_remove, inplace=True)
    classic_features.drop(indices_to_remove, inplace=True)
    fresh_features.drop(indices_to_remove, inplace=True)

    # Drop columns
    misc_features.drop(["framerate"], axis=1, inplace=True)
    misc_features.drop(["detection_time"], axis=1, inplace=True)
    misc_features.drop(["video_path"], axis=1, inplace=True)
    misc_features.drop(["hand"], axis=1, inplace=True)
    misc_features.drop(["handedness"], axis=1, inplace=True)

    # Impute
    impute(fresh_features)


def get_data(videos_dir, cache_dir=None):
    data_getter = DataGetter(videos_dir, cache_dir)
    y, misc_features, time_series = data_getter.get_input_data()

    # Extract classic features
    classic_settings = {
        mean_speed: None,
        frequency_of_maximums: None,
        frequency_of_minimums: None,
        average_of_maximums: None,
        std_of_maximums: None,
        slotted_difference_of_frequency_of_minimums: None,
        slotted_difference_of_average_of_maximums: None,
    }
    classic_features = extract_features(
        time_series, column_id="id", default_fc_parameters=classic_settings
    )

    # Extract TSFresh default features
    fresh_features = extract_features(time_series, column_id="id")

    return y, misc_features, classic_features, fresh_features
