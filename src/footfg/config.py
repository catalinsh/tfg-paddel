import logging

from pydantic import BaseSettings, Field

log = logging.getLogger(__name__)


class _Settings(BaseSettings):
    video_dir: str = Field("data/raw", env="FOOTFG_VIDEO_DIR")
    interim_dir: str = Field("data/interim", env="FOOTFG_INTERIM_DIR")


settings = _Settings()

log.info(f"Using the following settings:\n{settings}")
