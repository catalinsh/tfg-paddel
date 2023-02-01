import logging
from datetime import timedelta

from pydantic import BaseSettings, DirectoryPath

log = logging.getLogger(__name__)


class _Settings(BaseSettings):
    dirs__samples: DirectoryPath
    dirs__interim: DirectoryPath

    preprocessing__skip_done_samples: bool = True
    preprocessing__min_detection_time: timedelta = timedelta(seconds=10)

    class Config:
        env_prefix = "PADDEL_"


settings = _Settings()

log.info(f"Using the following settings:\n{settings}")
