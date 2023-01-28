from typing import NamedTuple

import numpy as np
import numpy.typing as npt

Image = npt.NDArray[np.uint8]


class Point(NamedTuple):
    x: float
    y: float
    z: float


class HandLandmarks(NamedTuple):
    WRIST: Point
    THUMB_CMC: Point
    THUMB_MCP: Point
    THUMB_IP: Point
    THUMB_TIP: Point
    INDEX_FINGER_MCP: Point
    INDEX_FINGER_PIP: Point
    INDEX_FINGER_DIP: Point
    INDEX_FINGER_TIP: Point
