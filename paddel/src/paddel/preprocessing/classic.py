from math import ceil
from typing import Sequence

import numpy as np
import numpy.typing as npt
import pandas as pd
from scipy.signal import find_peaks

from paddel import settings
from paddel.types import HandLandmarks


def angle_between(
    a_in: npt.ArrayLike,
    b_in: npt.ArrayLike,
    c_in: npt.ArrayLike,
) -> float:
    """Get angle between 3 points in n-dimensional euclidean
    space.
    :param a_in: First point.
    :param b_in: Second point.
    :param c_in: Third point.
    :return: Angle in radians, 0 if any of the point coincide.
    """
    a = np.asarray(a_in)
    b = np.asarray(b_in)
    c = np.asarray(c_in)

    if np.array_equal(a, b) or np.array_equal(a, c) or np.array_equal(b, c):
        return 0

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle: float = np.arccos(cosine_angle)

    return angle


def get_taps(angles: pd.Series, framerate: float) -> npt.NDArray[int]:
    """Get the amount of taps from the given hand angle series.

    :param angles: Series of angles.
    :param framerate: Framerate of the original video.
    :return: Array containing the positions of the taps.
    """
    window = ceil(framerate) * 3
    rolling_std = angles.rolling(window, center=True, min_periods=0).std().to_numpy()
    taps, _ = find_peaks(
        -angles.to_numpy(),
        prominence=rolling_std,
        height=(-settings.preprocessing.MAX_RADIANS_FOR_TAP, 0),
    )

    return taps


def get_tap_rate_difference(
    taps: npt.NDArray[int], frame_count: int, framerate: float
) -> float:
    """Get the tap rate difference between the first and last halves
    of the video.

    :param taps: Array containing the positions of the taps.
    :param frame_count: Number of frames of the original video.
    :param framerate: Framerate of the original video.
    :return: Difference in tapping rate.
    """
    middle = frame_count / 2
    tap_rate_1 = (taps < middle).sum() / framerate
    tap_rate_2 = (taps >= middle).sum() / framerate

    return abs(tap_rate_1 - tap_rate_2)


def extract_classic_features(
    landmarks: Sequence[HandLandmarks], framerate: float
) -> tuple[float, float]:
    """Extract different features from the landmarks sequence from previous works in the field.

    :param landmarks: Sequence of the video landmarks.
    :param framerate: Framerate of the video.
    :return: Tuple of features.
    """
    angles = pd.Series(
        [angle_between(lm.INDEX_FINGER_TIP, lm.WRIST, lm.THUMB_TIP) for lm in landmarks]
    )
    frame_count = len(landmarks)
    elapse_time = frame_count / framerate

    taps = get_taps(angles, framerate)
    tap_rate = len(taps) / elapse_time
    tap_rate_difference = get_tap_rate_difference(taps, frame_count, framerate)

    return tap_rate, tap_rate_difference
