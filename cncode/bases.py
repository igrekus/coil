from abc import ABC, abstractmethod
from enum import Enum

from euclid3 import Point2
from pygcode import Line


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
        LINE_TO_END, \
        LINE_TO_START, \
        LINE_TO_BOTH, \
        CW_ARC_TO_SHORT, \
        CW_ARC_TO_LONG, \
        CCW_ARC_TO_SHORT, \
        CCW_ARC_TO_LONG = range(24)


move_commands = [
    CommandType.LINE_TO,
    CommandType.LINE_TO_END,
    CommandType.LINE_TO_START,
    CommandType.LINE_TO_BOTH,
    CommandType.CW_ARC_TO_SHORT,
    CommandType.CW_ARC_TO_LONG,
    CommandType.CCW_ARC_TO_SHORT,
    CommandType.CCW_ARC_TO_LONG
]


class ArcType(Enum):
    SHORT, LONG = range(2)


arc_label = {ArcType.SHORT: 'Short', ArcType.LONG: 'Long'}


class Command(ABC):
    def __init__(self, type_: CommandType = CommandType.UNDEFINED, index: int=0, label: str='undefined', spill: float=0.0, delay: float=0.0, prm: float=0.0):
        self._type: CommandType = type_
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
        else:
            raise IndexError

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
    def from_string(cls, string: str, *args, **kwargs):
        pass

    @property
    def command_type(self):
        return self._type


class OneLineCommand(Command, ABC):
    def __init__(self, type_: CommandType = CommandType.UNDEFINED, index: int=0, label: str='undefined', prm: float=0.0):
        super().__init__(type_=type_,
                         index=index,
                         label=label,
                         spill=0.0,
                         delay=0.0,
                         prm=prm)

    def __str__(self):
        return f'{self.__class__.__name__}(index={self._index}, prm={self._prm})'

    def __getitem__(self, item):
        if item in range(2, 9):
            return ''
        elif item == 0:
            return self._index
        elif item == 1:
            return self._label
        elif item == 9:
            return self._prm
        else:
            raise IndexError

    @property
    def disabled(self):
        return 2, 3, 4, 5, 6, 7, 8

    @property
    @abstractmethod
    def as_gcode(self):
        pass

    @classmethod
    def from_string(cls, string: str, *args, **kwargs):
        cnc_lines = [Line(l) for l in string.strip().split('\n')]
        assert len(cnc_lines) == 1

        line1 = cnc_lines[0]
        assert line1.gcodes[0].word_letter == 'N'

        index = line1.gcodes[0].number
        prm = line1.block.modal_params[1].value
        return cls(index=index, prm=prm)


class MoveCommand(Command, ABC):
    def __init__(self, type_: CommandType = CommandType.UNDEFINED, index: int=0, label: str='undefined',
                 x: float=0.0, y: float=0.0, r: float=0.0, arc: ArcType=ArcType.SHORT,
                 speed: float=0.0, spill: float=0.0, delay: float=0.0, prm: float=0.0,
                 prev_gui_end: Point2=None, prev_gcode_end: Point2=None):
        super().__init__(type_=type_, index=index, label=label, spill=spill, delay=delay, prm=prm)
        self._r = r
        self._arc = arc
        self._speed = speed

        if not prev_gui_end:
            prev_gui_end = Point2()
        if not prev_gcode_end:
            prev_gcode_end = Point2()
        self._gui_p1 = prev_gui_end.copy()
        self._gcode_p1 = prev_gcode_end.copy()

        self._gui_p2 = Point2(x, y)

    def __str__(self):
        return f'AbstractMoveCommand()'

    def __getitem__(self, item):
        if item == 0:
            return self._index
        elif item == 1:
            return self._label
        elif item == 2:
            return self._gui_p2.x
        elif item == 3:
            return self._gui_p2.y
        elif item == 4:
            return self._r
        elif item == 5:
            return self._arc
        elif item == 6:
            return self._speed
        elif item == 7:
            return self._spill
        elif item == 8:
            return ''
        elif item == 9:
            return ''
        else:
            raise IndexError

    @property
    def disabled(self):
        return 8, 9

    @property
    @abstractmethod
    def gui_geometry(self):
        pass

    @property
    @abstractmethod
    def gcode_geometry(self):
        return list()

    @property
    @abstractmethod
    def as_gcode(self):
        pass

    @classmethod
    @abstractmethod
    def from_string(cls, string: str, *args, **kwargs):
        pass

    @property
    def is_move(self):
        return True

    @property
    def length(self):
        return sum(g.length for g in self.gcode_geometry)
