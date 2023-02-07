import hashlib
import pickle
from functools import wraps
from pathlib import Path
from typing import Callable

from paddel import settings


def get_file_hash(path: Path) -> str:
    """Get hash for the file in the given path.

    :param path: Path of file to hash.
    :return: File hash.
    """
    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


def path_input_cache(function: Callable) -> Callable:
    """Function wrapper that saves return value for the file in the given path.
    To identify each individual file, a sha256 hash of the file is utilized.

    :param function: Function to wrap.
    :return: Wrapped function.
    """

    @wraps(function)
    def wrapper(path, *args, **kwargs):
        file_hash = get_file_hash(path)
        function_cache_dir = settings.dirs.cache / function.__name__
        function_cache_dir.mkdir(exist_ok=True)
        out_path = function_cache_dir / file_hash

        if out_path.exists():
            with open(out_path, "rb") as f:
                return pickle.load(f)

        result = function(path, *args, **kwargs)

        with open(out_path, "wb") as f:
            pickle.dump(result, f)

        return result

    return wrapper
