import logging

from .config import settings

logging.getLogger(__name__).addHandler(logging.NullHandler())
