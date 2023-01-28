from mediapipe.python.solutions.hands import Hands  # type: ignore

from paddel.config import settings


def initialize_hands() -> Hands:
    return Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=settings.mediapipe_min_detection_confidence,
        min_tracking_confidence=settings.mediapipe_min_tracking_confidence,
    )
