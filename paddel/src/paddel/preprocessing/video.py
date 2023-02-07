from pathlib import Path

import cv2  # type: ignore

from paddel.types import Video


def read_video(path: Path) -> Video:
    """Iterate over the video frames from the video in the given path.

    :param path: Video path.
    :return: Video iterator.
    """
    video_capture = cv2.VideoCapture(str(path))

    if not video_capture.isOpened():
        video_capture.release()
        return []

    while video_capture.grab():
        bgr = video_capture.retrieve()[1]
        yield cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    video_capture.release()


def extract_video_frame_count(path: Path) -> int:
    """Extracts the video framerate from the video in
    the given path.

    :param path: Path to video.
    :return: Video framerate, -1 if file not readable.
    """
    video_capture = cv2.VideoCapture(str(path))

    if not video_capture.isOpened():
        video_capture.release()
        return -1

    frame_count = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    video_capture.release()

    return frame_count


def extract_video_framerate(path: Path) -> float:
    """Extracts the video framerate from the video in
    the given path.

    :param path: Path to video.
    :return: Video framerate, -1 if file not readable.
    """
    video_capture = cv2.VideoCapture(str(path))

    if not video_capture.isOpened():
        video_capture.release()
        return -1

    framerate = video_capture.get(cv2.CAP_PROP_FPS)
    video_capture.release()

    return framerate
