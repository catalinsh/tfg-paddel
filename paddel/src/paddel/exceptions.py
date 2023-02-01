class InvalidFilenameError(Exception):
    """Raised when a filename does not match the expected format."""


class NotAVideoError(Exception):
    """Raised when trying to read a file that is not a video as a video."""
