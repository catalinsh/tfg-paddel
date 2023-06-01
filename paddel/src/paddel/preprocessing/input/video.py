from pathlib import Path

import cv2  # type: ignore
import pandas as pd

from paddel.preprocessing.input.classic import extract_classic_features
from paddel.preprocessing.input.fresh import extract_fresh_features
from paddel.preprocessing.input.poses import extract_poses_ts
from paddel.preprocessing.input.time_series import extract_time_series


def extract_video_features(video_path: Path) -> tuple[pd.Series, pd.Series, float]:
    """Extract features from video at given path.

    Args:
        video_path (Path): Video path.

    Returns:
        tuple[pd.Series, pd.Series, float]: Video features.
    """
    poses_ts = extract_poses_ts(video_path)

    # If no poses detected
    if poses_ts.empty:
        return pd.Series(dtype=float), pd.Series(dtype=float), 0

    time_series = extract_time_series(poses_ts)
    time_series["id"] = 0  # id for tsfresh

    detection_time = (poses_ts.index[-1] - poses_ts.index[0]).total_seconds()

    classic_features = extract_classic_features(time_series)
    fresh_features = extract_fresh_features(time_series)

    return classic_features, fresh_features, detection_time
