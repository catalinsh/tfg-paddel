import logging

from pydantic import BaseModel, BaseSettings, DirectoryPath

log = logging.getLogger(__name__)


class Dirs(BaseModel):
    raw: DirectoryPath
    cache: DirectoryPath


class Settings(BaseSettings):
    dirs: Dirs

    class Config:
        env_prefix = "PADDEL_"
        env_nested_delimiter = "__"


settings = Settings()

log.info(f"Using the following settings:\n{settings.dict()}")
