from enum import Enum


class ObjectType(Enum):
    Line = 1
    TransformerLarge = 2
    TransformerMedium = 3
    Station = 4


class ControlCenter(Enum):
    NDC = 0
    ZG = 1
    RI = 2
    ST = 3
    OS = 4
