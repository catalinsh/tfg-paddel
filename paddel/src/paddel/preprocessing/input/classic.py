import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from tsfresh import extract_features
from tsfresh.feature_extraction.feature_calculators import set_property

from paddel import settings


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def mean_speed(x: pd.Series) -> float:
    """Obtains the main speed of the given time series.

    Args:
        x (pd.Series): Time series to obtain mean speed from.

    Returns:
        float: Mean speed of the time series (units/second).
    """
    time = x.index
    time_seconds = (time[-1] - time[0]).total_seconds()

    differences = np.abs(np.diff(x.to_numpy()))

    total_difference = np.sum(differences)

    return total_difference / time_seconds


def rolling_std_prominence_maximums(x: pd.Series) -> list:
    """Obtains the maximums of the given time series filtering them using a rolling standard deviation.

    Args:
        x (pd.Series): Series to get maximums from.

    Returns:
        list: Set of maximums.
    """
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
def frequency_of_maximums(x: pd.Series) -> float:
    """Obtains the frequency at which maximums happen within the given time series.

    Args:
        x (pd.Series): Time series to get maximum frequency from.

    Returns:
        float: Maximum frequency.
    """
    time = x.index
    maximums = rolling_std_prominence_maximums(x)
    time_seconds = (time[-1] - time[0]).total_seconds()

    return len(maximums) / time_seconds


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def frequency_of_minimums(x: pd.Series):
    """Obtains the frequency at which minimums happen within the given time series.

    Args:
        x (pd.Series): Time series to get minimum frequency from.

    Returns:
        float: Minimum frequency.
    """
    return frequency_of_maximums(-x)


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def average_of_maximums(x: pd.Series) -> float:
    """Average value of maximums from the given time series.

    Args:
        x (pd.Series): Time series to get average maximum from.

    Returns:
        float: Average of maximums.
    """
    maximums_idx = rolling_std_prominence_maximums(x)
    maximums = x[maximums_idx]
    return np.mean(maximums)


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def std_of_maximums(x: pd.Series) -> float:
    """Standard deviation value of maximums from the given time series.

    Args:
        x (pd.Series): Time series to get standard deviation of maximums from.

    Returns:
        float: Standard deviation of maximums.
    """
    maximums_idx = rolling_std_prominence_maximums(x)
    maximums = x[maximums_idx]
    return np.std(maximums)


def get_slots(x: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Obtains subsequences from given series for the features that requiere time slot comparison.

    Args:
        x (pd.Series): Time series to get slots from.

    Returns:
        tuple(pd.Series, pd.Series): Both slots.
    """
    slot_size = pd.to_timedelta(settings.slot_size_seconds, unit="seconds")
    start_slot_mark = x.index[0] + slot_size
    end_slot_mark = x.index[-1] - slot_size

    start_slot = x[:start_slot_mark]
    end_slot = x[end_slot_mark:]

    return start_slot, end_slot


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def slotted_difference_of_frequency_of_minimums(x: pd.Series) -> float:
    """Get de difference between the frequency of minimums in the slots.

    Args:
        x (pd.Series): Series to get frequence difference from.

    Returns:
        float: Minimum frequence difference.
    """
    start_slot, end_slot = get_slots(x)
    return frequency_of_minimums(start_slot) - frequency_of_minimums(end_slot)


@set_property("fctype", "simple")
@set_property("input", "pd.Series")
@set_property("index_type", pd.DatetimeIndex)
def slotted_difference_of_average_of_maximums(x: pd.Series) -> float:
    """Get de difference between the frequency of maximums in the slots.

    Args:
        x (pd.Series): Series to get frequence difference from.

    Returns:
        float: Maximum frequence difference.
    """
    start_slot, end_slot = get_slots(x)
    return average_of_maximums(start_slot) - average_of_maximums(end_slot)


def extract_classic_features(time_series: pd.DataFrame) -> pd.Series:
    """Extract time series features.

    Args:
        time_series (pd.DataFrame): Time series to extract features from.

    Returns:
        pd.Series: Extracted features.
    """
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
        time_series,
        column_id="id",
        default_fc_parameters=classic_settings,
        n_jobs=1,
        disable_progressbar=True,
    )

    return classic_features.iloc[0]
