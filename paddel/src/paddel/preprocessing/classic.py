from math import ceil, floor
from typing import Sequence

import numpy as np
import numpy.typing as npt
import pandas as pd
from scipy.signal import find_peaks
from scipy.stats import variation

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
    """Get the position of the taps in the given hand angle series.

    :param angles: Series of angles.
    :param framerate: Framerate of the original video.
    :return: Array containing the positions of the taps.
    """
    window = ceil(framerate) * 3
    rolling_std = angles.rolling(window, center=True, min_periods=0).std().to_numpy()

    taps, _ = find_peaks(
        -angles.to_numpy(),
        prominence=rolling_std,
        height=(-settings.preprocessing.max_radians_for_tap, 0),
    )
    return taps


def get_amplitudes(angles: pd.Series, framerate: float) -> npt.NDArray[int]:
    """Get the positions where the hand is at maximum amplitude in
    the given angle series.

    :param angles: Series of angles.
    :param framerate: Framerate of the original video.
    :return: Array containing the positions of the amplitudes.
    """
    window = ceil(framerate) * 3
    rolling_std = angles.rolling(window, center=True, min_periods=0).std().to_numpy()

    taps, _ = find_peaks(
        angles.to_numpy(),
        prominence=rolling_std,
        height=settings.preprocessing.max_radians_for_tap,
    )
    return taps


def get_average_speed(angles: pd.Series, framerate: float) -> float:
    """Get average speed, measured as the rate of change per second.

    :param angles: Series of angles.
    :param framerate: Framerate of the original video.
    :return: Average speed measured in radians per second.
    """
    changes = np.abs(np.diff(angles))
    average = np.mean(changes)

    # Times framerate to account for framerate differences.
    average_per_second = average * framerate
    return average_per_second


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
    first_third = frame_count / 3
    second_third = (frame_count * 2) / 3
    tap_rate_1 = (taps <= first_third).sum() / framerate
    tap_rate_2 = (taps >= second_third).sum() / framerate

    return abs(tap_rate_1 - tap_rate_2)


def extract_classic_features(
    landmarks: Sequence[HandLandmarks], framerate: float
) -> dict[str, float]:
    """Extract different features from the landmarks sequence from previous works in the field.

    :param landmarks: Sequence of the video landmarks.
    :param framerate: Framerate of the video.
    :return: Tuple of features.
    """
    angles = pd.Series(
        [
            angle_between(lm.INDEX_FINGER_TIP, lm.THUMB_MCP, lm.THUMB_TIP)
            for lm in landmarks
        ]
    )
    frame_count = len(landmarks)
    elapse_time = frame_count / framerate

    # Taps
    taps = get_taps(angles, framerate)
    taps_slot1 = taps[taps < frame_count / 3]
    taps_slot2 = taps[taps > frame_count * 2 / 3]

    tap_rate = len(taps) / elapse_time
    tap_rate_difference = (len(taps_slot1) - len(taps_slot2)) / (elapse_time / 3)

    # Amplitudes
    amplitudes = get_amplitudes(angles, framerate)
    amplitudes_slot1 = amplitudes[amplitudes < frame_count / 3]
    amplitudes_slot2 = amplitudes[amplitudes > frame_count * 2 / 3]

    amplitude_average = np.mean(angles[amplitudes])
    amplitude_variation = variation(angles[amplitudes], axis=None)
    amplitude_difference = np.mean(angles[amplitudes_slot1]) - np.mean(
        angles[amplitudes_slot2]
    )
    amplitude_difference = (
        amplitude_difference if not np.isnan(amplitude_difference) else 0
    )

    # Speed
    speed = get_average_speed(angles, framerate)
    speed_slot1 = get_average_speed(angles[: floor(framerate / 3)], framerate)
    speed_slot2 = get_average_speed(angles[-floor(framerate / 3) :], framerate)
    speed_difference = speed_slot1 - speed_slot2

    angle_average = np.mean(angles)

    return {
        "tap_rate": tap_rate,
        "tap_rate_difference": tap_rate_difference,
        "amplitude_variation": amplitude_variation,
        "amplitude_average": amplitude_average,
        "amplitude_difference": amplitude_difference,
        "speed": speed,
        "speed_difference": speed_difference,
        "angle_average": angle_average,
    }
