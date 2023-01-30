from enum import IntEnum, auto


class Side(IntEnum):
    LEFT = 0
    RIGHT = auto()


class IndividualType(IntEnum):
    CONTROL = 0
    ID = auto()


class Gender(IntEnum):
    FEMALE = 0
    MALE = auto()