from typing import Sequence, Any

from mediapipe.python.solutions.hands import Hands  # type: ignore

from paddel.config import settings
from paddel.preprocessing.image_landmark_extraction import extract_image_landmarks
from paddel.types import Video, HandLandmarks


def initialize_hands() -> Hands:
    return Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=settings.mediapipe_min_detection_confidence,
        min_tracking_confidence=settings.mediapipe_min_tracking_confidence,
    )


def get_longest_non_none_sequence(sequence: Sequence[Any]) -> Sequence[Any]:
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
    with initialize_hands() as hands:
        landmarks = [extract_image_landmarks(image, hands) for image in video]

    return get_longest_non_none_sequence(landmarks)
