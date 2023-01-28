import math

import cv2
import numpy as np
import pytest

from paddel.preprocessing.image_landmark_extraction import (
    extract_image_landmarks,
)
from paddel.preprocessing.video_landmark_extraction import (
    initialize_hands,
    extract_video_landmarks,
)
from paddel.types import HandLandmarks

hand_open_image: np.ndarray = cv2.imread("tests/resources/hand_open.jpg")
hand_open_image = hand_open_image[..., [2, 1, 0]]

hand_closed_image: np.ndarray = cv2.imread("tests/resources/hand_closed.jpg")
hand_closed_image = hand_closed_image[..., [2, 1, 0]]

blank_image: np.ndarray = cv2.imread("tests/resources/blank.jpg")
blank_image = blank_image[..., [2, 1, 0]]


def _distance(p0: tuple, p1: tuple) -> float:
    return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2 + (p0[2] - p1[2]) ** 2)


def test_landmark_image():
    with initialize_hands() as hands:
        landmarks_open = extract_image_landmarks(hand_open_image, hands)
        assert landmarks_open
        assert type(landmarks_open) == HandLandmarks

        landmarks_closed = extract_image_landmarks(hand_closed_image, hands)
        assert landmarks_closed
        assert type(landmarks_closed) == HandLandmarks

        open_hand_index_thumb_distance = _distance(
            landmarks_open.THUMB_TIP,
            landmarks_open.INDEX_FINGER_TIP,
        )

        closed_hand_index_thumb_distance = _distance(
            landmarks_closed.THUMB_TIP,
            landmarks_closed.INDEX_FINGER_TIP,
        )

        assert closed_hand_index_thumb_distance < open_hand_index_thumb_distance

        assert not extract_image_landmarks(blank_image, hands)


@pytest.mark.parametrize(
    "video,length",
    [
        (
            [
                hand_open_image,
                hand_closed_image,
                hand_open_image,
                hand_closed_image,
            ],
            4,
        ),
        (
            [
                hand_open_image,
                blank_image,
                hand_open_image,
                hand_closed_image,
            ],
            2,
        ),
        (
            [
                hand_open_image,
                hand_closed_image,
                blank_image,
                hand_open_image,
                hand_closed_image,
            ],
            2,
        ),
        (
            [
                blank_image,
                hand_open_image,
                hand_closed_image,
            ],
            2,
        ),
        (
            [
                hand_open_image,
                hand_closed_image,
                blank_image,
            ],
            2,
        ),
        (
            [
                blank_image,
                blank_image,
                blank_image,
                blank_image,
            ],
            0,
        ),
    ],
)
def test_landmark_video(video, length):
    landmarks = extract_video_landmarks(video)
    assert len(landmarks) == length
    assert all(type(lm) == HandLandmarks for lm in landmarks)
