from typing import Optional

import numpy as np
import numpy.typing as npt
from mediapipe.python.solutions.hands import Hands  # type: ignore

from paddel.config import settings
from paddel.enums import Landmark
from paddel.types import HandLandmarks


def initialize_hands() -> Hands:
    return Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=settings.mediapipe_min_detection_confidence,
        min_tracking_confidence=settings.mediapipe_min_tracking_confidence,
    )


def extract_image_landmarks(
    image: npt.NDArray[np.uint8], hands: Hands
) -> Optional[HandLandmarks]:
    hands_result = hands.process(image)

    # If hand not detected, retry, this time without
    # tracking landmarks from previous image
    if not hands_result.multi_hand_landmarks:
        hands_result = hands.process(image)

    if not hands_result.multi_hand_landmarks:
        return None

    hand_result = hands_result.multi_hand_landmarks[0]

    landmarks = hand_result.landmark

    wanted_landmarks = []

    for wanted_index in Landmark:
        landmark = (
            landmarks[wanted_index].x,
            landmarks[wanted_index].y,
            landmarks[wanted_index].z,
        )
        wanted_landmarks.append(landmark)

    return wanted_landmarks
