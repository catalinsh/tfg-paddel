import logging

from .config import settings as settings

logging.getLogger(__name__).addHandler(logging.NullHandler())
