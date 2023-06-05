import pickle
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Union

import pandas as pd

from paddel import settings
from paddel.preprocessing.input.features import extract_features


def _get_cache_paths(cache_dir: Path) -> tuple[Path, Path, Path]:
    """Get cache paths for the different datasets.

    Args:
        cache_dir (Path): Base cache path.

    Returns:
        tuple[Path, Path, Path]: Cached datasets paths.
    """
    misc_df_path = cache_dir / "misc_df.pkl"
    classic_df_path = cache_dir / "classic_df.pkl"
    fresh_df_path = cache_dir / "fresh_df.pkl"

    return misc_df_path, classic_df_path, fresh_df_path


def _load_pkl(file_path: Path) -> Union[pd.DataFrame, None]:
    """Load pickled object from given path

    Args:
        file_path (Path): Path to the pickle binary file.

    Returns:
        Union[pd.DataFrame, None]: Loaded object.
    """
    if not file_path.exists():
        return pd.DataFrame()
    with open(file_path, "rb") as f:
        return pickle.load(f)


def _load_cache(cache_dir: Path) -> tuple:
    """Load all datasets from cache.

    Args:
        cache_dir (Path): Base cache path.

    Returns:
        tuple: Loaded datasets.
    """
    if cache_dir:
        misc_df_path, classic_df_path, fresh_df_path = _get_cache_paths(cache_dir)

        misc_df = _load_pkl(misc_df_path)
        classic_df = _load_pkl(classic_df_path)
        fresh_df = _load_pkl(fresh_df_path)
    else:
        misc_df = pd.DataFrame()
        classic_df = pd.DataFrame()
        fresh_df = pd.DataFrame()

    return misc_df, classic_df, fresh_df


def _save_pkl(file_path: Path, data: Any):
    """Save given data as pickle object in given path.

    Args:
        file_path (Path): File to save data to.
        data (Any): Data to save.
    """
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


def _save_cache(
    cache_dir: Path,
    misc_df: pd.DataFrame,
    classic_df: pd.DataFrame,
    fresh_df: pd.DataFrame,
):
    """Save datasets to cache.

    Args:
        cache_dir (Path): Cache base directory.
        misc_df (pd.DataFrame): Miscelaneous dataframe.
        classic_df (pd.DataFrame): Classic dataframe.
        fresh_df (pd.DataFrame): TSFresh dataframe.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    misc_df_path, classic_df_path, fresh_df_path = _get_cache_paths(cache_dir)

    _save_pkl(misc_df_path, misc_df)
    _save_pkl(classic_df_path, classic_df)
    _save_pkl(fresh_df_path, fresh_df)


def _get_cached_video_names(misc_df: pd.DataFrame) -> set[str]:
    """Get video paths of videos that are already cached.

    Args:
        misc_df (pd.DataFrame): Miscelaneous dataframe.

    Returns:
        set[Path]: Cached videos paths.
    """
    if "video_path" in misc_df:
        return set([p.name for p in misc_df["video_path"]])
    else:
        return set()


def get_input_data(
    videos_dir: Path, cache_dir: Path
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Get raw data to use to train the models.

    Args:
        videos_dir (Path): Directory where the videos are located.
        cache_dir (Path, optional): Directory to store cached data. Defaults to Path().

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Loaded data.
    """
    misc_df, classic_df, fresh_df = _load_cache(cache_dir)

    video_names = set([p.name for p in videos_dir.iterdir()])
    cached_video_names = _get_cached_video_names(misc_df)
    missing_video_names = video_names - cached_video_names
    missing_video_paths = set([videos_dir / n for n in missing_video_names])

    if not missing_video_paths:
        return misc_df, classic_df, fresh_df

    with Pool(settings.max_processes) as p:
        results = p.map(extract_features, missing_video_paths)

    results_misc, results_classic, results_fresh = zip(*results)

    misc_df = pd.concat([misc_df, pd.DataFrame(results_misc)], ignore_index=True)
    classic_df = pd.concat(
        [classic_df, pd.DataFrame(results_classic)], ignore_index=True
    )
    fresh_df = pd.concat([fresh_df, pd.DataFrame(results_fresh)], ignore_index=True)

    if cache_dir:
        _save_cache(cache_dir, misc_df, classic_df, fresh_df)

    return misc_df, classic_df, fresh_df
