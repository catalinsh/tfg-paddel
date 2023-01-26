from pathlib import Path

from paddel.preprocessing.filename_features import extract_filename_features


def test_bad_filenames():
    assert extract_filename_features(Path("")) is None
