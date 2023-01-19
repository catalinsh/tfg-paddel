import time
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import Callable

import cv2
import numpy as np


class FileVideoStream:
    def __init__(self, path: Path, transform: Callable = None, queue_size: int = 8):
        """Class that accelerates video file decoding with the use of multithreading to
        utilize IO waiting times.

        :param path: Path of the video to be read
        :param transform: Function to apply to each frame before return
        :param queue_size: Size of the queue to be used
        :raises TypeError: If given path is not readable by OpenCV
        """
        self.video_capture = cv2.VideoCapture(str(path))

        if not self.video_capture.isOpened():
            self.video_capture.release()
            raise TypeError(f"OpenCV can't read {path}, is it a video?")

        self.transform = transform

        self.frame_queue = Queue(maxsize=queue_size)

        self.thread = Thread(target=self.__queue_frames, args=())
        self.thread.daemon = True

        self.should_stop = False
        # Grab now in case of video with no frames
        self.has_frames_left = self.video_capture.grab()

    def __enter__(self):
        """Allows usage of this class with 'with' statement. Implements start
        behaviour and starts the thread execution.

        :return: self
        """
        self.thread.start()
        return self

    def __exit__(self, *args):
        """Allows usage of this class with 'with' statement. Implements exit
        behaviour and waits for the thread to stop.

        :param args: Unused arguments
        """
        # Allows thread to be stopped mid-execution
        self.should_stop = True
        self.thread.join()

    def __queue_frames(self):
        """Method executed by the extra thread, it puts read frames into the queue."""
        while not self.should_stop:
            if self.frame_queue.full():
                time.sleep(0.1)
                continue

            if not self.has_frames_left:
                break

            frame = self.video_capture.retrieve()[1]

            if self.transform:
                frame = self.transform(frame)

            self.frame_queue.put(frame)

            self.has_frames_left = self.video_capture.grab()

        self.video_capture.release()

    def read(self) -> np.ndarray:
        """Obtains the next transformed frame from the queue.

        :return: Next frame
        """
        return self.frame_queue.get()
