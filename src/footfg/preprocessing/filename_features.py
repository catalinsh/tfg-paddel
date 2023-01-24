import logging
import re
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


def extract_filename_features(path: Path) -> Optional[dict[str, str]]:
    filename = path.name.rpartition(".")[0]

    # TODO:
    #  Check ambidextrous
    pattern = re.compile(
        r'(?P<id>(?:CONTROL|ID)\d+)'
        r'_'
        r'(?P<date>\d{2}-\d{2}-\d{4})'
        r'_'
        r'(?P<hand>\w+)'
        r' '
        r'\('
        r'(?P<gender>[MH])'
        r'-'
        r'(?P<age>\w+)'
        r'-'
        r'(?P<handedness>[DZ])'
        r'\)'
    )

    match = pattern.match(filename)

    if not match:
        log.warning(f"Could not match filename of {path}")
        return None

    return match.groupdict()
