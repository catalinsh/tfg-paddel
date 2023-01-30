import os
from tempfile import TemporaryDirectory

import cv2
import numpy as np
import pytest

from paddel.preprocessing.video import read_video
from paddel.types import Image

hand_open_image: Image = cv2.imread("tests/resources/hand_open.jpg")

hand_closed_image: Image = cv2.imread("tests/resources/hand_closed.jpg")

blank_image: Image = cv2.imread("tests/resources/blank.jpg")


@pytest.mark.parametrize(
    "video",
    [
        ([hand_open_image, hand_closed_image, blank_image]),
        ([]),
        ([hand_open_image]),
    ],
)
def test_read_video(video):
    width, height, _ = hand_open_image.shape
    directory = TemporaryDirectory()

    path = os.path.join(directory.name, "video.avi")

    # RGBA for no compression
    video_writer = cv2.VideoWriter(
        path, cv2.VideoWriter_fourcc(*"RGBA"), 30, (width, height)
    )

    for image in video:
        video_writer.write(image)

    video_writer.release()

    # Switch to RGB
    video = [image[..., [2, 1, 0]] for image in video]

    video_got = list(read_video(path))

    assert len(video_got) == len(video)
    assert all(np.array_equal(got, expected) for got, expected in zip(video_got, video))

    directory.cleanup()
