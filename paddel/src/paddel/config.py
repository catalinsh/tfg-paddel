import logging
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, DirectoryPath

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    videos_dir: DirectoryPath
    cache_dir: Optional[Path]

    max_radians_for_tap: float = 0.2
    min_detection_seconds: float = 15

    max_processes: int = os.cpu_count()

    class Config:
        env_prefix = "PADDEL_"


settings = Settings()

log.info(f"Using the following settings:\n{settings.dict()}")
