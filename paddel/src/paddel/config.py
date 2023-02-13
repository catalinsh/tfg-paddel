import logging

from pydantic import BaseModel, BaseSettings

log = logging.getLogger(__name__)


class Preprocessing(BaseModel):
    max_radians_for_tap: float = 0.2
    min_detection_seconds: float = 15


class Settings(BaseSettings):
    preprocessing: Preprocessing = Preprocessing()

    class Config:
        env_prefix = "PADDEL_"
        env_nested_delimiter = "__"


settings = Settings()

log.info(f"Using the following settings:\n{settings.dict()}")
