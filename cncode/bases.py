from abc import ABC
from enum import Enum

from euclid3 import Point2


class Command(ABC):
    def __init__(self, text, previous=None):
        self._text: str = text
        self._lines: list = text.split('\n')

        self._type: CommandType = CommandType.UNDEFINED
        self._previous: Command = previous
        self._geom_start_point: Point2 = Point2(0, 0) if not previous else self._previous._geom_end_point.copy()

        self._cnc_lines: list = list()

        self._geom_end_point: Point2 = self._geom_start_point.copy()
        self._geom_primitives = list()

        self._index: int = 0
        self._label: str = 'undefined'
        self._spill: float = 0.0   # first P parameter
        self._delay: float = 0.0   # second P parameter
        self._prm: float = 0.0   # arbitrary parameter
        self._x: float = 0.0
        self._y: float = 0.0
        self._r: float = 0.0
        self._speed: float = 0.0
        self._arc_type: ArcType = ArcType.SHORT

    def __str__(self):
        return f'CnCommand(type={self._type})'

    def __getitem__(self, item):
        if item == 0:
            return self._index
        elif item == 1:
            return self._label
        elif item == 2:
            return self._x
        elif item == 3:
            return self._y
        elif item == 4:
            return self._r
        elif item == 5:
            return arc_label[self._arc_type]
        elif item == 6:
            return self._speed
        elif item == 7:
            return self._spill
        elif item == 8:
            return self._delay
        elif item == 9:
            return self._prm

    def _parse(self):
        self._cnc_lines = [Line(l) for l in self._lines]

    def shift(self, direction, value):
        pass

    def shift_start(self, direction, value):
        print('shift start', self, direction, value)

    def shift_end(self, direction, value):
        print('shift end', self, direction, value)

    @property
    def enabled(self):
        return ()

    @property
    def length(self):
        return 0

    @property
    def p1(self):
        return Point2(self._geom_start_point.x, self._geom_start_point.y)

    @property
    def p2(self):
        return Point2(self._geom_end_point.x, self._geom_end_point.y)

    @staticmethod
    def from_lines(text, previous):
        lines = text.split('\n')
        length = len(lines)
        if length == 1:
            line = lines[0]
            if 'M70' in line:
                return WeldCommand(text=text, previous=previous)
            elif 'M71' in line:
                return SonoUpCommand(text=text, previous=previous)
            elif 'M72' in line:
                return SonoMidCommand(text=text, previous=previous)
            elif 'M73' in line:
                return SonoLowCommand(text=text, previous=previous)
            elif 'M74' in line:
                return CutWireCommand(text=text, previous=previous)
            elif 'M75' in line:
                return EmbedOnCommand(text=text, previous=previous)
            elif 'M76' in line:
                return EmbedOffCommand(text=text, previous=previous)
            elif 'M77' in line:
                return PullWireCommand(text=text, previous=previous)
            elif 'M78' in line:
                return HoldModuleCommand(text=text, previous=previous)
            elif 'M79' in line:
                return ReleaseModuleCommand(text=text, previous=previous)
            elif 'M80' in line:
                return BrakeOnCommand(text=text, previous=previous)
            elif 'M81' in line:
                return BrakeOffCommand(text=text, previous=previous)
            elif 'M82' in line:
                return ThermMidCommand(text=text, previous=previous)
            elif 'M83' in line:
                return ThermUpCommand(text=text, previous=previous)
        elif length == 2:
            return FillCommand(text=text, previous=previous)
        elif length == 3:
            line1, line2, line3 = lines
            if 'G01' in line3:
                return LineToCommand(text=text, previous=previous)
            elif 'G02' in line3:
                return ArcToCommand(text=text, previous=previous, arc_type=ArcType.SHORT, arc_dir=ArcDirection.CW)
            elif 'G03' in line3:
                return ArcToCommand(text=text, previous=previous, arc_type=ArcType.SHORT, arc_dir=ArcDirection.CCW)
        elif length == 4:
            # long arc = arc + arc
            *_, line3, line4 = lines
            if 'G01' not in line3 and 'G01' not in line4:
                if 'G02' in line3 and 'G02' in line4:
                    return ArcToCommand(text=text, previous=previous, arc_type=ArcType.LONG, arc_dir=ArcDirection.CW)
                elif 'G03' in line3 and 'G03' in line4:
                    return ArcToCommand(text=text, previous=previous, arc_type=ArcType.LONG, arc_dir=ArcDirection.CCW)
            # line + end arc
            elif 'G01' in line3 and 'G01' not in line4:
                return LineToWithEndCurveCommand(text=text, previous=previous)
            # start arc + line
            elif 'G01' not in line3 and 'G01' in line4:
                return LineToWithStartCurveCommand(text=text, previous=previous)
        elif length == 5:
            return LineToWithBothCurvesCommand(text=text, previous=previous)
        else:
            return Command(text=text, previous=previous)

    @property
    def is_move(self):
        return False

    @property
    def as_gcode(self):
        raise NotImplementedError
