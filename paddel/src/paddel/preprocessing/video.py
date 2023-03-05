from pathlib import Path

import cv2  # type: ignore

from paddel.types import Video


def is_video(path: Path) -> bool:
    """Check if file in given path is readable by OpenCV.

    :param path: Path to file to check.
    :return: If file is video.
    """
    video_capture = cv2.VideoCapture()
    video_capture.setExceptionMode(True)

    try:
        video_capture.open(str(path))

        ret = video_capture.isOpened()
        video_capture.release()

        return ret
    except cv2.error:
        return False


def read_video(path: Path) -> Video:
    """Iterate over the video frames from the video in the given path.
    It's expected for the path to point to a valid video file.

    :param path: Video path.
    :return: Video iterator.
    """
    video_capture = cv2.VideoCapture(str(path))

    while video_capture.grab():
        bgr = video_capture.retrieve()[1]
        yield cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    video_capture.release()


def get_framerate(path: Path) -> float:
    """Extracts the video framerate from the video in
    the given path. It's expected for the path to point to
    a valid video file.

    :param path: Path to video.
    :return: Video framerate, -1 if file not readable.
    """
    video_capture = cv2.VideoCapture(str(path))

    framerate = video_capture.get(cv2.CAP_PROP_FPS)
    video_capture.release()

    return framerate
