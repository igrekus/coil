from abc import ABC, abstractmethod
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


arc_label = {ArcType.SHORT: 'Short', ArcType.LONG: 'Long'}


class Command(ABC):
    def __init__(self, type_: CommandType = CommandType.UNDEFINED, index: int=0, label: str='undefined', spill: float=0.0, delay: float=0.0, prm: float=0.0):
        self._type: type_
        self._index: int = index
        self._label: str = label
        self._spill: float = spill   # first P parameter
        self._delay: float = delay   # second P parameter
        self._prm: float = prm       # arbitrary parameter

    def __str__(self):
        return f'AbstractCommand()'

    def __getitem__(self, item):
        if item == 0:
            return self._index
        elif item == 1:
            return self._label
        elif item == 2:
            return ''
        elif item == 3:
            return ''
        elif item == 4:
            return ''
        elif item == 5:
            return ''
        elif item == 6:
            return ''
        elif item == 7:
            return self._spill
        elif item == 8:
            return self._delay
        elif item == 9:
            return self._prm

    @property
    @abstractmethod
    def disabled(self):
        pass

    @property
    def length(self):
        return 0

    @property
    def is_move(self):
        return False

    @property
    @abstractmethod
    def as_gcode(self):
        pass

    @classmethod
    @abstractmethod
    def from_string(cls, string: str):
        pass
