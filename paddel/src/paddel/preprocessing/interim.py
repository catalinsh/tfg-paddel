import logging
import os.path
import pickle
from pathlib import Path
from typing import Any, Iterable, Sequence

from paddel import settings
from paddel.exceptions import InvalidFilenameError, NotAVideoError
from paddel.preprocessing.filename import extract_filename_features
from paddel.preprocessing.landmark import extract_video_landmarks
from paddel.preprocessing.video import extract_video_features
from paddel.types import HandLandmarks

log = logging.getLogger(__name__)


def get_interim_path(path: Path) -> Path:
    """Get destination path for interim data of file in given path.

    :param path: Original sample file.
    :return: Interim destination path.
    """
    filename = path.name.rpartition(".")[0]
    return Path(os.path.join(settings.dirs__interim, filename))


def is_sample_done(path: Path) -> bool:
    """Check if there is already interim data for given path.

    :param path: Original sample file.
    :return: If the is interim data.
    """
    interim_path = get_interim_path(path)
    return interim_path.exists() and interim_path.is_file()


def extract_interim_data(path: Path) -> tuple[dict[str, Any], Sequence[HandLandmarks]]:
    """Extract filename features, video features, and landmarks.

    :param path: Sample path.
    :return: Dictionary with features and landmarks.
    """
    filename_features = extract_filename_features(path.name)

    video_features = extract_video_features(path)

    features = filename_features | video_features

    landmarks = extract_video_landmarks(path)

    features["landmark_count"] = len(landmarks)

    return features, landmarks


def save_interim_data(
    path: Path, features: tuple[dict[str, Any], Sequence[HandLandmarks]]
) -> None:
    """Extract features from the sample and save them to their apropiate location.

    :param features:
    :param path: File to extract features from.
    :return: None.
    :raises InvalidFilenameError: If filename is not valid.
    :raises NotAVideoError: If file is not a video.
    """
    with open(get_interim_path(path), "wb") as file:
        pickle.dump(features, file)


def preprocess_interim() -> None:
    """Iterates over the sample directory obtaining sample features and
    landmarks for posterior preprocessing phases.

    :return: None.
    """
    samples = settings.dirs__samples.iterdir()

    for sample_path in samples:
        if is_sample_done(sample_path):
            log.info(f"{sample_path} already has interim data. Skipping.")
            continue

        try:
            interim_data = extract_interim_data(sample_path)
        except (InvalidFilenameError, NotAVideoError):
            log.exception(f"{sample_path} feature extraction failed. Skipping.")
            continue

        save_interim_data(sample_path, interim_data)
        log.info(f"{sample_path} feature extraction was successful.")


def load_interim_items() -> Iterable[tuple[dict[str, Any], Sequence[HandLandmarks]]]:
    """Generator the iterates over the interim data.

    :return: Interim data generator.
    """
    item_paths = settings.dirs__interim.iterdir()

    for item_path in item_paths:
        with open(item_path, "rb") as file:
            yield pickle.load(file)
