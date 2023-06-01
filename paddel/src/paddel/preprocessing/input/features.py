import logging
from pathlib import Path

import pandas as pd

from paddel.preprocessing.input.misc import extract_misc_features
from paddel.preprocessing.input.video import extract_video_features

log = logging.getLogger(__name__)


def extract_features(video_path: Path) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Extract features from video at given path.

    Args:
        video_path (Path): Path of video.

    Returns:
        tuple[pd.Series, pd.Series, pd.Series]: Video features.
    """
    log.info(f'Extracting features from "{video_path}".')

    misc_features = extract_misc_features(video_path)
    (
        classic_features,
        fresh_features,
        misc_features["detection_time"],
    ) = extract_video_features(video_path)

    return misc_features, classic_features, fresh_features
