import os


def test_environment_configuration():
    data = [
        ("PADDEL_VIDEO_DIR", "video_dir", "/video/directory"),
        ("PADDEL_INTERIM_DIR", "interim_dir", "/interim/directory"),
    ]

    for env_key, _, value in data:
        os.environ[env_key] = str(value)

    from paddel.config import settings

    for _, config_key, value in data:
        assert getattr(settings, config_key) == value
