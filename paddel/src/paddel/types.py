from typing import Iterable, NamedTuple

import numpy as np
import numpy.typing as npt

Image = npt.NDArray[np.uint8]
Video = Iterable[Image]


class Point(NamedTuple):
    x: float
    y: float
    z: float


Pose = dict[str, Point]
