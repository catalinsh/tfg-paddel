from typing import Any, Sequence

from mediapipe.python.solutions.hands import Hands  # type: ignore

from paddel.config import settings
from paddel.preprocessing.image_landmark_extraction import extract_image_landmarks
from paddel.types import HandLandmarks, Video


def initialize_hands() -> Hands:
    """Initialize Mediapipe Hands object.

    :return: Mediapipe Hands object.
    """
    return Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=settings.mediapipe_min_detection_confidence,
        min_tracking_confidence=settings.mediapipe_min_tracking_confidence,
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


def extract_video_landmarks(video: Video) -> Sequence[HandLandmarks]:
    """Extract hand landmarks from the given video.

    :param video: Video to landmark.
    :return: Video landmarks.
    """
    with initialize_hands() as hands:
        landmarks = [extract_image_landmarks(image, hands) for image in video]

    return get_longest_non_none_sequence(landmarks)
