from pathlib import Path

import cv2  # type: ignore

from paddel.types import Video


def read_video(path: Path) -> Video:
    """Iterate over the video frames from the video in the given path.

    :param path: Video path.
    :return: Generator that iterates over the frames.
    """
    video_capture = cv2.VideoCapture(str(path))
    while video_capture.grab():
        bgr = video_capture.retrieve()[1]
        yield cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    video_capture.release()
