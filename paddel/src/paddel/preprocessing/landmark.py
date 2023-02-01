from pathlib import Path
from typing import Any, Optional, Sequence

import cv2  # type: ignore
from mediapipe.python.solutions.hands import Hands  # type: ignore

from paddel.preprocessing.video import read_video
from paddel.types import HandLandmarks, Image, Point


def extract_image_landmarks(image: Image, hands: Hands) -> Optional[HandLandmarks]:
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

    hand_result = hands_result.multi_hand_landmarks[0]

    mediapipe_landmarks = hand_result.landmark[0:9]

    landmarks = HandLandmarks(*(Point(lm.x, lm.y, lm.z) for lm in mediapipe_landmarks))

    return landmarks


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


def get_longest_non_none_sequence(sequence: Sequence[Any]) -> Sequence[Any]:
    """Get the longest not None valued sequence from the given sequence.

    :param sequence: Sequence to operate on.
    :return: Longest non-None sequence.
    """
    current: list[Any] = []
    best: list[Any] = []

    for item in sequence:
        if item:
            current.append(item)
        elif len(current) > len(best):
            best = current
            current = []
        else:
            current = []

    if len(current) > len(best):
        best = current

    return best


def extract_video_landmarks(video_path: Path) -> Sequence[HandLandmarks]:
    """Extract hand landmarks from the given file path.

    :param video_path: Video path to landmark.
    :return: Video landmarks.
    :raises: NotAVideoError: If the file in the given path is not a video.
    """
    video = read_video(video_path)

    with initialize_hands() as hands:
        landmarks = [extract_image_landmarks(image, hands) for image in video]

    return get_longest_non_none_sequence(landmarks)
