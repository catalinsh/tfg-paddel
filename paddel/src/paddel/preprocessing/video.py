from numbers import Number
from pathlib import Path

import cv2  # type: ignore

from paddel.exceptions import NotAVideoError
from paddel.types import Video


def read_video(path: Path) -> Video:
    """Iterate over the video frames from the video in the given path.
    It is expected for the path to point to a valid video file.

    :param path: Video path.
    :return: Generator that iterates over the frames.
    :raises: NotAVideoError: If path not a video.
    """
    video_capture = cv2.VideoCapture(str(path))
    if not video_capture.isOpened():
        video_capture.release()
        raise NotAVideoError(f"OpenCV cannot read {path} as a video.")

    while video_capture.grab():
        bgr = video_capture.retrieve()[1]
        yield cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    video_capture.release()


def extract_video_features(path: Path) -> dict[str, Number]:
    """Get various video features from the given path.
    It is expected for the path to point to a valid video file.

    :param path: Video path.
    :return: Video features.
    :raises: NotAVideoError: If path not a video.
    """
    video_capture = cv2.VideoCapture(str(path))
    if not video_capture.isOpened():
        video_capture.release()
        raise NotAVideoError(
            f"Cannot extract features from {path} OpenCV cannot read this file."
        )

    ret = {
        "width": int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "frames_count": int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        "framerate": video_capture.get(cv2.CAP_PROP_FPS),
        "fourcc": int(video_capture.get(cv2.CAP_PROP_FOURCC)),
    }
    video_capture.release()
    return ret
