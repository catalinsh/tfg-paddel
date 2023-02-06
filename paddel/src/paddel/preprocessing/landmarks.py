import logging
import pickle
from pathlib import Path
from typing import Optional, Sequence

from mediapipe.python.solutions.hands import Hands  # type: ignore

from paddel.preprocessing.video import read_video
from paddel.types import HandLandmarks, Image, Point

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


def get_longest_non_none_sequence(
    sequence: Sequence[HandLandmarks | None],
) -> Sequence[HandLandmarks]:
    """Get the longest not None valued sequence from the given sequence.

    :param sequence: Sequence to operate on.
    :return: Longest non-None sequence.
    """
    current: list = []
    best: list = []

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


def load_landmarks(landmarks_path: str) -> Sequence[HandLandmarks]:
    """Load landmarks from given path.

    :param landmarks_path: Path with the landmarks.
    :return: Landmark sequence.
    """
    with open(landmarks_path, "rb") as file:
        return pickle.load(file)


def extract_landmarks(
    video_path: str, landmarks_path: str | None = None
) -> Sequence[HandLandmarks]:
    """Extract hand landmarks from the given file path into the given landmark path.

    :param video_path: Video path.
    :param landmarks_path: Path to pickle file to save or load the landmarks.
    :return: Video landmarks.
    """
    if landmarks_path and Path(landmarks_path).exists():
        return load_landmarks(landmarks_path)

    video = read_video(video_path)

    with initialize_hands() as hands:
        extracted_landmarks = [extract_image_landmarks(image, hands) for image in video]

    landmarks = get_longest_non_none_sequence(extracted_landmarks)

    log.info(f"Extracted landmarks from {video_path} successfully.")

    if landmarks_path:
        with open(landmarks_path, "wb") as file:
            pickle.dump(landmarks, file)

    return landmarks
