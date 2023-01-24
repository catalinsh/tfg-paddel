import logging
from pathlib import Path

from footfg.preprocessing.filename_features import extract_filename_features

log = logging.getLogger(__name__)


def extract_features(path: Path):
    log.info(f"Extracting features from {path}.")

    filename_features = extract_filename_features(path)

    return filename_features
