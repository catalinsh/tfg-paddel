import logging

from pydantic import BaseSettings, Field

log = logging.getLogger(__name__)


class _Settings(BaseSettings):
    video_dir: str = Field("data/raw", env="PADDEL_VIDEO_DIR")
    interim_dir: str = Field("data/interim", env="PADDEL_INTERIM_DIR")
    mediapipe_min_detection_confidence: float = Field(
        "0.5", env="PADDEL_MEDIAPIPE_MIN_DETECTION_CONFIDENCE"
    )
    mediapipe_min_tracking_confidence: float = Field(
        "0.5", env="PADDEL_MEDIAPIPE_MIN_TRACKING_CONFIDENCE"
    )


settings = _Settings()

log.info(f"Using the following settings:\n{settings}")
