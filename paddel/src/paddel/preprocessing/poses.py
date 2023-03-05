import logging
from pathlib import Path
from typing import Iterable, Optional

import cv2  # type: ignore
import pandas as pd
from mediapipe.python.solutions.hands import Hands  # type: ignore

from paddel.types import Image, Point, Pose

from .video import read_video

log = logging.getLogger(__name__)


def initialize_hands() -> Hands:
    """Initialize Mediapipe Hands object.

    :return: Mediapipe Hands object.
    """
    return Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )


def extract_image_pose(image: Image, hands: Hands) -> Optional[Pose]:
    """Extract hand landmarks from the given image.

    :param image: Image to extract landmarks from.
    :param hands: Mediapipe Hands object.
    :return: Image landmarks or None.
    """
    hands_result = hands.process(image)

    # If hand not detected, retry, this time without
    # tracking landmarks from previous image
    if not hands_result.multi_hand_landmarks:
        hands_result = hands.process(image)

    if not hands_result.multi_hand_landmarks:
        return None

    landmarks = hands_result.multi_hand_landmarks[0].landmark

    pose = {
        "WRIST": Point(landmarks[0].x, landmarks[0].y, landmarks[0].z),
        "THUMB_CMC": Point(landmarks[1].x, landmarks[1].y, landmarks[1].z),
        "THUMB_MCP": Point(landmarks[2].x, landmarks[2].y, landmarks[2].z),
        "THUMB_IP": Point(landmarks[3].x, landmarks[3].y, landmarks[3].z),
        "THUMB_TIP": Point(landmarks[4].x, landmarks[4].y, landmarks[4].z),
        "INDEX_FINGER_MCP": Point(landmarks[5].x, landmarks[5].y, landmarks[5].z),
        "INDEX_FINGER_PIP": Point(landmarks[6].x, landmarks[6].y, landmarks[6].z),
        "INDEX_FINGER_DIP": Point(landmarks[7].x, landmarks[7].y, landmarks[7].z),
        "INDEX_FINGER_TIP": Point(landmarks[8].x, landmarks[8].y, landmarks[8].z),
    }

    return pose


def longest_non_none_sequence(poses: Iterable[Optional[Pose]]) -> list[Pose]:
    current: list[Pose] = []
    best: list[Pose] = []

    for pose in poses:
        if pose:
            current.append(pose)
        elif len(current) > len(best):
            best = current
            current = []
        else:
            current = []

    if len(current) > len(best):
        best = current

    return best


def extract_poses(path: Path) -> list[Pose]:
    """Extract hand landmarks from the given file path into the given landmark path.
    It's expected for the path to point to a valid video file.

    :param path: Video path.
    :return: Video landmarks.
    """
    log.info(f'Extracting landmarks from "{path}".')

    video = read_video(path)

    with initialize_hands() as hands:
        poses = map(lambda image: extract_image_pose(image, hands), video)

        return longest_non_none_sequence(poses)


def extract_poses_ts(row: pd.Series) -> pd.DataFrame:
    poses = extract_poses(row["video_path"])

    index = [(frame / row["framerate"]) * 10e8 for frame in range(len(poses))]
    index = pd.DatetimeIndex(index)

    df = pd.DataFrame(poses, index=index)

    return df
