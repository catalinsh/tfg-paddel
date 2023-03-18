import logging
import os

from pydantic import BaseSettings

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    min_detection_seconds: float = 15
    # Window size for rolling standard deviation used in feature calculations
    rolling_std_seconds: float = 3
    # Used for slotted feature calculations, size of beginning and end slots
    # should not be more than 1/2 of min_detection_seconds
    slot_size_seconds: float = 7

    max_processes: int = os.cpu_count()

    class Config:
        env_prefix = "PADDEL_"


settings = Settings()

log.info(f"Using the following settings:\n{settings.dict()}")
