import numpy as np
import numpy.typing as npt
import pandas as pd


@np.vectorize
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


def extract_time_series(poses: pd.DataFrame) -> pd.DataFrame:
    ts_df = pd.DataFrame()

    ts_df["angle"] = angle_between(
        poses["THUMB_TIP"], poses["WRIST"], poses["INDEX_FINGER_TIP"]
    )

    ts_df.index = poses.index
    return ts_df
