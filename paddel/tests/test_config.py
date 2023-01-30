import importlib
import os

import paddel.config


def test_environment_configuration():
    data = [
        ("PADDEL_VIDEO_DIR", "video_dir", "/video/directory"),
        ("PADDEL_INTERIM_DIR", "interim_dir", "/interim/directory"),
        (
            "PADDEL_MEDIAPIPE_MIN_DETECTION_CONFIDENCE",
            "mediapipe_min_detection_confidence",
            1.6180,
        ),
        (
            "PADDEL_MEDIAPIPE_MIN_TRACKING_CONFIDENCE",
            "mediapipe_min_tracking_confidence",
            2.7183,
        ),
    ]

    for env_key, _, value in data:
        os.environ[env_key] = str(value)

    # reload to update config from environment
    importlib.reload(paddel.config)

    for _, config_key, value in data:
        assert getattr(paddel.config.settings, config_key) == value
