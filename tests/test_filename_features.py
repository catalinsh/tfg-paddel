from paddel.enums import IndividualType, Side, Gender
from paddel.preprocessing.filename_features import extract_filename_features


def test_valid_filenames():
    features = extract_filename_features("CONTROL279_00-00-0000_DCH (M-22-Z).mp4")
    assert features
    assert features["individual_type"] == IndividualType.CONTROL
    assert features["hand"] == Side.RIGHT
    assert features["gender"] == Gender.FEMALE
    assert features["age"] == 22
    assert features["handedness"] == Side.LEFT

    features = extract_filename_features("id2807_12-24-2048_iz (h-XX-D).MOV")
    assert features
    assert features["individual_type"] == IndividualType.ID
    assert features["hand"] == Side.LEFT
    assert features["gender"] == Gender.MALE
    assert features["age"] == -1
    assert features["handedness"] == Side.RIGHT


def test_invalid_filenames():
    features = extract_filename_features("ctrl279_00-00-0000_DCH (M-22-Z).mp4")
    assert not features

    features = extract_filename_features("CONTROL279_00-00-0000_dz (M-22-Z).mp4")
    assert not features

    features = extract_filename_features("CONTROL279_00-00-0000_DCH (V-22-Z).mp4")
    assert not features

    features = extract_filename_features("CONTROL279_00-00-0000_DCH (M-22-L).mp4")
    assert not features

    features = extract_filename_features(".mp4")
    assert not features
