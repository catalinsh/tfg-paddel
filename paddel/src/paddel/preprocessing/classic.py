from math import ceil
from typing import Sequence

import numpy as np
import numpy.typing as npt
import pandas as pd
from scipy.signal import find_peaks

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


def get_tap_rate(framerate: float, angles: pd.Series) -> float:
    """Get the tap rate of the given angles at the given framerate.
    A tap is considered as a local minimum in the angles time series,
    in order to remove undesired minimums a rolling standard deviation
    is used to determine the prominence necessary for a minimum to be
    considered as such.

    :param framerate: Framerate of the video the angles come from.
    :param angles: Pandas series to get tap_rate_from
    :return: Tapping rate in taps per second.
    """

    window = ceil(framerate) * 3
    rsd = angles.rolling(window, center=True, min_periods=0).std().to_numpy() * 1.9

    tap_number = len(find_peaks(-angles.to_numpy(), prominence=rsd)[0])
    elapsed_time = len(angles) / framerate
    tap_rate = tap_number / elapsed_time

    return tap_rate


def extract_classic_features(
    framerate: float, landmarks: Sequence[HandLandmarks]
) -> pd.Series:
    """Extract features used in previous works in the field.

    :param framerate: Framerate of the video the landmarks come from.
    :param landmarks: Landmarks to extract features from.
    :return: Series of different features.
    """
    angles = pd.Series(
        [
            angle_between(lm.INDEX_FINGER_TIP, lm.WRIST, lm.THUMB_TIP)
            for lm in landmarks
        ],
    )

    features = {"tap_rate": get_tap_rate(framerate, angles)}

    return pd.Series(features, dtype=float)
