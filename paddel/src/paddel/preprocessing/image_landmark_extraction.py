from typing import Optional

from mediapipe.python.solutions.hands import Hands  # type: ignore

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
