import logging
from pathlib import Path
from typing import Sequence

import cv2  # type: ignore
from mediapipe.python.solutions.hands import Hands  # type: ignore

from paddel.decorators import path_input_cache
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


def extract_image_landmarks(image: Image, hands: Hands) -> HandLandmarks | None:
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

    def length(interval):
        return interval[1] - interval[0]

    current = [0, 0]
    best = [0, 0]

    for item in sequence:
        if item is not None:
            current[1] += 1
        elif length(current) > length(best):
            best = current
            current = [best[1] + 1, best[1] + 1]
        else:
            current = [current[1] + 1, current[1] + 1]

    if length(current) > length(best):
        best = current

    return sequence[best[0] : best[1]]


@path_input_cache
def extract_landmarks(path: Path) -> Sequence[HandLandmarks]:
    """Extract hand landmarks from the given file path into the given landmark path.

    :param path: Video path.
    :return: Video landmarks.
    """
    log.info(f'Extracting landmarks from "{path}".')

    video = read_video(path)

    with initialize_hands() as hands:
        extracted_landmarks = [extract_image_landmarks(image, hands) for image in video]

    landmarks = get_longest_non_none_sequence(extracted_landmarks)

    return landmarks
