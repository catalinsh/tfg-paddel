import math

import cv2
import numpy as np

from paddel.enums import Landmark
from paddel.preprocessing.image_landmark_extraction import (
    extract_image_landmarks,
    initialize_hands,
)

hand_open_image: np.ndarray = cv2.imread("tests/resources/hand_open.jpg")
hand_open_image = hand_open_image[..., [2, 1, 0]]

hand_closed_image: np.ndarray = cv2.imread("tests/resources/hand_closed.jpg")
hand_closed_image = hand_closed_image[..., [2, 1, 0]]

blank_image: np.ndarray = cv2.imread("tests/resources/blank.jpg")
blank_image = blank_image[..., [2, 1, 0]]


def _distance(p0, p1):
    return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2 + (p0[2] - p1[2]) ** 2)


def test_landmark_image():
    with initialize_hands() as hands:
        landmarks_open = extract_image_landmarks(hand_open_image, hands)
        assert landmarks_open
        assert len(landmarks_open) == len(Landmark)

        landmarks_closed = extract_image_landmarks(hand_closed_image, hands)
        assert landmarks_closed
        assert len(landmarks_closed) == len(Landmark)

        open_hand_index_thumb_distance = _distance(
            landmarks_open[Landmark.THUMB_TIP],
            landmarks_open[Landmark.INDEX_FINGER_TIP],
        )

        closed_hand_index_thumb_distance = _distance(
            landmarks_closed[Landmark.THUMB_TIP],
            landmarks_closed[Landmark.INDEX_FINGER_TIP],
        )

        assert closed_hand_index_thumb_distance < open_hand_index_thumb_distance

        assert not extract_image_landmarks(blank_image, hands)
