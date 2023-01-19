import sys

REQUIRED_PYTHON = (3, 9)


def check_python_virtual_environment():
    base_prefix = (
        getattr(sys, "base_prefix", None)
        or getattr(sys, "real_prefix", None)
        or sys.prefix
    )
    current_prefix = sys.prefix

    if base_prefix == current_prefix:
        raise TypeError(
            "It looks like you are not in a virtual environment, "
            "this project works best if you are in one, so please switch to one."
        )


def check_python_version():
    found_python = (sys.version_info.major, sys.version_info.minor)

    if REQUIRED_PYTHON != found_python:
        raise TypeError(
            "This project requires Python {}. Found: Python {}".format(
                ".".join(map(str, REQUIRED_PYTHON)),
                ".".join(map(str, found_python)),
            )
        )


if __name__ == "__main__":
    check_python_virtual_environment()
    check_python_version()
