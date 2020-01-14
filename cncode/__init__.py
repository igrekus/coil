from enum import Enum


class CommandType(Enum):
    UNDEFINED, \
        FILL, \
        WELD, \
        SONO_UP, \
        SONO_MID, \
        SONO_LOW, \
        CUT_WIRE, \
        EMBED_ON, \
        EMBED_OFF, \
        PULL_WIRE, \
        HOLD_MODULE, \
        RELEASE_MODULE, \
        BRAKE_ON, \
        BRAKE_OFF, \
        THERM_MID, \
        THERM_UP, \
        LINE_TO, \
        CW_ARC_TO, \
        CCW_ARC_TO, \
        LINE_TO_END, \
        LINE_TO_START, \
        LINE_TO_BOTH = range(22)


move_commands = [
    CommandType.LINE_TO,
    CommandType.CW_ARC_TO,
    CommandType.CCW_ARC_TO,
    CommandType.LINE_TO_END,
    CommandType.LINE_TO_START,
    CommandType.LINE_TO_BOTH
]


class ArcType(Enum):
    SHORT, LONG = range(2)


class ArcDirection(Enum):
    CW, CCW = range(2)
