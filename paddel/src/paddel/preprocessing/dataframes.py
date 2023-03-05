import pickle
from multiprocessing import Pool
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from paddel import settings

from .filename import extract_filename_features
from .poses import extract_poses_ts
from .time_series import angle_between
from .video import get_framerate, is_video


def extract_features(video_path: Path) -> Optional[tuple]:
    # Check if video
    if not is_video(video_path):
        return None

    # Extract features from file
    misc_features = pd.Series(extract_filename_features(video_path))
    misc_features["video_path"] = video_path
    misc_features["framerate"] = get_framerate(video_path)

    if misc_features["group"] == -1:
        return None
    if misc_features["hand"] == -1:
        return None
    if misc_features["handedness"] == -1:
        return None

    misc_features["dominant_hand"] = (
        misc_features["hand"] == misc_features["handedness"]
    )

    y = pd.Series(misc_features["group"])
    misc_features.drop("group", inplace=True)

    # Extract hand poses
    poses_ts = extract_poses_ts(misc_features)

    # Get detection time
    misc_features["detection_time"] = len(poses_ts.index) / misc_features["framerate"]

    # Extract target time series from poses
    angles_ts = pd.Series(
        np.vectorize(angle_between)(
            poses_ts["THUMB_TIP"],
            poses_ts["WRIST"],
            poses_ts["INDEX_FINGER_TIP"],
        ),
        name="angle",
    )

    target_ts = pd.concat([angles_ts], axis=1).set_index(poses_ts.index)

    return y, misc_features, target_ts


def get_cache():
    if settings.cache_dir:
        y_file = settings.cache_dir / "y.pkl"
        misc_features_file = settings.cache_dir / "misc_features.pkl"
        target_ts_file = settings.cache_dir / "poses_ts.pkl"

        if y_file.exists() and misc_features_file.exists() and target_ts_file.exists():
            with open(y_file, "rb") as f:
                all_y = pickle.load(f)
            with open(misc_features_file, "rb") as f:
                all_misc_features = pickle.load(f)
            with open(target_ts_file, "rb") as f:
                all_target_ts = pickle.load(f)

            return all_y, all_misc_features, all_target_ts

    all_y = pd.Series(dtype=int)
    all_misc_features = pd.DataFrame()
    all_target_ts = pd.DataFrame()
    return all_y, all_misc_features, all_target_ts


def save_cache(all_y, all_file_features, all_target_ts):
    if not settings.cache_dir:
        return

    settings.cache_dir.mkdir(exist_ok=True, parents=True)

    y_file = settings.cache_dir / "y.pkl"
    misc_features_file = settings.cache_dir / "misc_features.pkl"
    target_ts_file = settings.cache_dir / "poses_ts.pkl"

    with open(y_file, "wb") as f:
        pickle.dump(all_y, f)

    with open(misc_features_file, "wb") as f:
        pickle.dump(all_file_features, f)

    with open(target_ts_file, "wb") as f:
        pickle.dump(all_target_ts, f)


def get_input_data():
    all_y, all_misc_features, all_target_ts = get_cache()

    video_paths = set(settings.videos_dir.iterdir())

    if "video_path" in all_misc_features:
        processed_video_paths = set(all_misc_features["video_path"])
        missing_video_paths = video_paths - processed_video_paths
    else:
        missing_video_paths = video_paths

    with Pool(settings.max_processes) as p:
        results = p.map(extract_features, missing_video_paths)

    filtered = [res for res in results if res is not None]

    # If there is new data to add
    if filtered:
        y, misc_features, target_ts = zip(*filtered)

        # Add ids to time series
        for idx, item in enumerate(target_ts):
            item["id"] = idx

        all_y = pd.concat([all_y, *y], ignore_index=True)
        all_misc_features = pd.concat(
            [all_misc_features, pd.DataFrame(misc_features)], ignore_index=True
        )
        all_target_ts = pd.concat([all_target_ts, *target_ts])

        save_cache(all_y, all_misc_features, all_target_ts)

    return all_y, all_misc_features, all_target_ts
