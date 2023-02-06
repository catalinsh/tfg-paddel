import cv2  # type: ignore
import numpy as np

from paddel.types import Video


def read_video(path: str) -> Video:
    """Iterate over the video frames from the video in the given path.

    :param path: Video path.
    :return: Video iterator.
    """
    video_capture = cv2.VideoCapture(path)

    if not video_capture.isOpened():
        video_capture.release()
        return []

    while video_capture.grab():
        bgr = video_capture.retrieve()[1]
        yield cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    video_capture.release()


def extract_video_framerate(path: str) -> float:
    """Extracts the video framerate from the video in
    the given path.

    :param path: Path to video.
    :return: Video framerate, NaN if file not readable.
    """
    video_capture = cv2.VideoCapture(path)

    if not video_capture.isOpened():
        video_capture.release()
        return np.nan

    framerate = video_capture.get(cv2.CAP_PROP_FPS)
    video_capture.release()

    return framerate
