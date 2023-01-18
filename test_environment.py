import sys

REQUIRED_PYTHON = (3, 9)

if __name__ == "__main__":
    found_python = (sys.version_info.major, sys.version_info.minor)

    if REQUIRED_PYTHON != found_python:
        raise TypeError(
            "This project requires Python {}. Found: Python {}".format(
                ".".join(map(str, REQUIRED_PYTHON)),
                ".".join(map(str, found_python)),
            )
        )
