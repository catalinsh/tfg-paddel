import datetime
import sys
from itertools import groupby
from math import floor
from pathlib import Path
from typing import Iterable, Dict, Optional, Union, List

import cv2
import numpy as np
import pandas as pd
from mediapipe.python.solutions.hands import Hands, HandLandmark

from filevideostream import FileVideoStream

# Minimum detection time for a video to be considered useful and be processed.
MIN_DETECTION_TIME = datetime.time(second=5)

# Landmarks that should be taken
WANTED_LANDMARK_INDICES = [
    HandLandmark.WRIST,
    HandLandmark.THUMB_CMC,
    HandLandmark.THUMB_MCP,
    HandLandmark.THUMB_IP,
    HandLandmark.THUMB_TIP,
    HandLandmark.INDEX_FINGER_MCP,
    HandLandmark.INDEX_FINGER_PIP,
    HandLandmark.INDEX_FINGER_DIP,
    HandLandmark.INDEX_FINGER_TIP,
]


def rotate_if_portrait(frame: np.ndarray) -> np.ndarray:
    """If the frame is in portrait, rotate it 180 degrees.

    :param frame: Frame to rotate
    :return: Rotated frame
    """
    height = frame.shape[0]
    width = frame.shape[1]
    is_portrait = width < height

    if is_portrait:
        frame = cv2.rotate(frame, cv2.ROTATE_180)

    return frame


def bgr_to_rgb(frame: np.ndarray) -> np.ndarray:
    """Converts a bgr(blue-green-red) frame to a rgb one.

    :param frame: Frame to be converted
    :return: RGB frame
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


def adjust_frame(frame: np.ndarray) -> np.ndarray:
    """Convert frame from cv2 format to be compatible with Mediapipe.

    :param frame: OpenCV frame
    :return: Converted frame
    """
    frame = rotate_if_portrait(frame)
    frame = bgr_to_rgb(frame)
    return frame


def read_video(path: Path) -> Iterable[np.ndarray]:
    """Obtains frames from video in given path.

    :param path: Video path
    :return: Video frames
    """
    with FileVideoStream(path, transform=adjust_frame) as file_video_stream:
        while file_video_stream.has_frames_left:
            yield file_video_stream.read()


def get_video_info(path: Path) -> Dict[str, Union[int, float]]:
    """Gets information about the video in the given path.

    :param path: Video path
    :return: Video information
    """
    vc = cv2.VideoCapture(str(path))

    info = {
        "width": int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "frame_count": int(vc.get(cv2.CAP_PROP_FRAME_COUNT)),
        "framerate": vc.get(cv2.CAP_PROP_FPS),
        "fourcc": int(vc.get(cv2.CAP_PROP_FOURCC)),
    }

    vc.release()
    return info


def initialize_hands() -> Hands:
    """Obtains a configured Mediapipe hands object.

    :return: Mediapipe hands object
    """
    return Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )


def landmark_frame(hands: Hands, frame: np.ndarray) -> Optional[Dict]:
    """Obtains the landmarks that correspond to the frame. If a frame could not be
    processed to obtain the landmarks, returns None.

    :param hands: Mediapipe hands object to use
    :param frame: Frame to landmark
    :return: Frame landmarks or None if frame not processed
    """
    hands_result = hands.process(frame)

    # If hand not detected, retry, this time without
    # tracking landmarks from previous image
    if not hands_result.multi_hand_landmarks:
        hands_result = hands.process(frame)

    if not hands_result.multi_hand_landmarks:
        return None

    hand_result = hands_result.multi_hand_landmarks[0]

    landmarks = hand_result.landmark

    wanted_landmarks = {}

    for wanted_index in WANTED_LANDMARK_INDICES:
        wanted_landmarks[wanted_index.name] = (
            landmarks[wanted_index].x,
            landmarks[wanted_index].y,
            landmarks[wanted_index].z,
        )

    return wanted_landmarks


def landmark_video(video: Iterable[np.ndarray]) -> List[Optional[Dict]]:
    """Obtains a list with the landmarks of each frame of the given video.

    :param video: Iterable of frames
    :return: Video landmarks
    """
    hands = initialize_hands()

    landmarks = [landmark_frame(hands, frame) for frame in video]

    hands.close()

    return landmarks


def add_frame_time_to_landmarks(landmarks: List[Optional[Dict]], framerate: float):
    """Adds the frame time to the given landmarks according to the framerate.

    :param landmarks: List of landmarks to give time to
    :param framerate: Framerate of the original video
    """
    for index, landmark in enumerate(landmarks):
        if not landmark:
            continue
        frame_time = index / framerate
        landmark["TIME"] = frame_time


def get_longest_landmarks_sequence(landmarks: List[Optional[Dict]]) -> List[Dict]:
    """Returns the longest sequence of not None values from a list.

    :param landmarks: List of landmarks and None
    :return: Longest non-None sequence
    """
    landmarks_groups = groupby(landmarks, lambda x: x is None)
    landmarks_lists = [list(group) for k, group in landmarks_groups if not k]

    # Get list with max length
    longest_landmarks_sequence = max(landmarks_lists, key=len)

    return longest_landmarks_sequence


if __name__ == "__main__":
    # Check video directory
    video_dir = Path(sys.argv[1]).absolute()

    if not video_dir.exists():
        video_dir.mkdir(parents=True, exist_ok=True)
        raise Exception(
            f"Directory {video_dir} does not exist, it has been create for you."
        )

    if not video_dir.is_dir():
        raise Exception(f"{video_dir} is not a directory!")

    video_files = list(video_dir.iterdir())
    if not video_files:
        raise Exception(
            f"Directory {video_dir} is empty, "
            f"make sure to put the video files there!"
        )

    # Create landmark directory
    landmark_dir = Path(sys.argv[2])
    landmark_dir.mkdir(parents=True, exist_ok=True)

    for video_path in video_dir.iterdir():
        csv_filename = video_path.name.rpartition(".")[0] + ".csv"
        csv_path = landmark_dir.joinpath(csv_filename)
        if csv_path.exists():
            print(f">>> {video_path.name}: CSV file already exists, skipping...")
            continue

        video_landmarks = landmark_video(read_video(video_path))
        video_landmarks = get_longest_landmarks_sequence(video_landmarks)

        video_framerate = get_video_info(video_path)["framerate"]
        min_frames_needed = floor(video_framerate * MIN_DETECTION_TIME.second)

        if len(video_landmarks) < min_frames_needed:
            print(
                f">>> {video_path.name}: not enough valid frames, "
                f"needed: {min_frames_needed}, got {len(video_landmarks)}, skipping..."
            )
            continue

        add_frame_time_to_landmarks(video_landmarks, video_framerate)

        print(f">>> {video_path.name}: landmark extraction successful, saving data...")

        dataframe = pd.DataFrame(video_landmarks)
        dataframe.to_csv(csv_path, index=False)
