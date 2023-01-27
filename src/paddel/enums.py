from enum import IntEnum, auto


class Landmark(IntEnum):
    WRIST = 0
    THUMB_CMC = auto()
    THUMB_MCP = auto()
    THUMB_IP = auto()
    THUMB_TIP = auto()
    INDEX_FINGER_MCP = auto()
    INDEX_FINGER_PIP = auto()
    INDEX_FINGER_DIP = auto()
    INDEX_FINGER_TIP = auto()


class Side(IntEnum):
    LEFT = 0
    RIGHT = auto()


class IndividualType(IntEnum):
    CONTROL = 0
    ID = auto()


class Gender(IntEnum):
    FEMALE = 0
    MALE = auto()
