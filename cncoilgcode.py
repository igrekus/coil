import os
import math

from enum import Enum
from euclid3 import Point2, Line2, LineSegment2, Circle
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


class Arc(Circle):
    def __init__(self, center: Point2, radius: float, p1: Point2, p2: Point2):
        super().__init__(center=center, radius=radius)
        self.p1 = p1.copy()
        self.p2 = p2.copy()

    def __str__(self):
        return f'Arc(<{self.c.x:.2f}>, <{self.c.y:.2f}>, ' \
               f'radius={self.r:.2f}, ' \
               f'start=(<{self.p1.x:.2f}>, <{self.p1.y:.2f}>) ' \
               f'end=(<{self.p2.x:.2f}>, <{self.p2.y:.2f}>))'

    @property
    def length(self):
        b = LineSegment2(self.p1, self.c).length
        c = LineSegment2(self.p2, self.c).length
        a = LineSegment2(self.p1, self.p2).length
        cosa = (pow(b, 2) + pow(c, 2) - pow(a, 2)) / \
               (2 * b * c)
        angle = math.acos(cosa)
        return self.r * angle


arc_label = {ArcType.SHORT: 'Short', ArcType.LONG: 'Long'}


class Command:
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


class FillCommand(Command):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Fill'
        self._type = CommandType.FILL

        self._parse()

    def __str__(self):
        return f'FillCnCommand(n={self._index} p1={self._spill} p2={self._delay})'

    def __getitem__(self, item):
        if item in range(2, 7):
            return ''
        elif item == 0:
            return self._index
        elif item == 1:
            return self._label
        elif item == 7:
            return self._spill
        elif item == 8:
            return self._delay
        elif item == 9:
            return ''

    def _parse(self):
        super()._parse()
        assert len(self._cnc_lines) == 2

        line1, line2 = self._cnc_lines
        assert line1.gcodes[0].word_letter == 'N'
        assert line2.gcodes[0].word == 'G04'

        self._index = line1.gcodes[0].number
        self._spill = line1.block.modal_params[1].value
        self._delay = line1.block.modal_params[2].value * 1000

    @property
    def enabled(self):
        return 1, 7, 8


class OneLineCommand(Command):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'undefined one-line command'
        self._type = CommandType.UNDEFINED

        self._parse()

    def __str__(self):
        return f'{self.__class__.__name__}(n={self._index} prm={self._prm})'

    def __getitem__(self, item):
        if item in range(2, 9):
            return ''
        elif item == 0:
            return self._index
        elif item == 1:
            return self._label
        elif item == 9:
            return self._prm

    def _parse(self):
        super()._parse()
        assert len(self._cnc_lines) == 1

        line1 = self._cnc_lines[0]
        assert line1.gcodes[0].word_letter == 'N'

        self._index = line1.gcodes[0].number
        self._spill = self._prm = line1.block.modal_params[1].value
        self._delay = line1.block.modal_params[2].value

    @property
    def enabled(self):
        return 1, 9


class WeldCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Weld'
        self._type = CommandType.WELD


class SonoUpCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Sono Up'
        self._type = CommandType.SONO_UP


class SonoMidCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Sono Mid'
        self._type = CommandType.SONO_MID


class SonoLowCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Sono Low'
        self._type = CommandType.SONO_LOW


class CutWireCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Cut wire'
        self._type = CommandType.CUT_WIRE


class EmbedOnCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Embed on'
        self._type = CommandType.EMBED_ON


class EmbedOffCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Embed off'
        self._type = CommandType.EMBED_OFF


class PullWireCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Pull wire'
        self._type = CommandType.PULL_WIRE


class HoldModuleCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Hold module'
        self._type = CommandType.HOLD_MODULE


class ReleaseModuleCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Release module'
        self._type = CommandType.RELEASE_MODULE


class BrakeOnCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Brake on'
        self._type = CommandType.BRAKE_ON


class BrakeOffCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Brake off'
        self._type = CommandType.BRAKE_OFF


class ThermMidCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Therm mid'
        self._type = CommandType.THERM_MID


class ThermUpCommand(OneLineCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Therm up'
        self._type = CommandType.THERM_UP


# TODO make move base command
class LineToCommand(Command):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Line To'
        self._type = CommandType.LINE_TO

        self._parse()

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'n={self._index} ' \
               f'x={self._x} ' \
               f'y={self._y} ' \
               f'r={self._r} ' \
               f'sp={self._speed} ' \
               f'p1={self._spill} ' \
               f'l={self.length})'

    def __getitem__(self, item):
        ret = super().__getitem__(item)
        if item == 4:
            ret = '*'
        return ret

    @property
    def length(self):
        return sum(p.length for p in self._geom_primitives)

    @property
    def enabled(self):
        return 1, 2, 3, 4, 6, 7

    @property
    def is_move(self):
        return True

    def _parse(self):
        super()._parse()

        line1, line2, line3 = self._cnc_lines

        self._index = line1.gcodes[0].number
        self._spill = line1.block.modal_params[1].value
        self._speed = line2.gcodes[0].word.value

        params = line3.gcodes[0].params
        self._geom_end_point = Point2(params['X'].value, params['Y'].value)

        self._x = self._geom_end_point.x
        self._y = self._geom_end_point.y

        self._geom_primitives.append(LineSegment2(self._geom_start_point, self._geom_end_point))

    def shift(self, direction, value):
        new_start_x, new_start_y = self._geom_start_point.x, self._geom_start_point.y
        new_end_x, new_end_y = self._geom_end_point.x, self._geom_end_point.y
        if direction == 'right':
            new_start_x += value
            new_end_x += value
        elif direction == 'left':
            new_start_x -= value
            new_end_x -= value
        elif direction == 'up':
            new_start_y += value
            new_end_y += value
        elif direction == 'down':
            new_start_y -= value
            new_end_y -= value

        new_end_point = Point2(new_end_x, new_end_y)
        new_start_point = Point2(new_start_x, new_start_y)

        self._geom_start_point = new_start_point
        self._geom_end_point = new_end_point

        self._x = self._geom_end_point.x
        self._y = self._geom_end_point.y

        self._geom_primitives.clear()
        self._geom_primitives.append(LineSegment2(self._geom_start_point, self._geom_end_point))

    @property
    def as_gcode(self):
        return f'N{self._index:03d}'


class ArcToCommand(Command):
    def __init__(self, text, previous=None, arc_type=ArcType.SHORT, arc_dir=ArcDirection.CW):
        super().__init__(text, previous)
        self._label = 'CW Arc To' if arc_dir else 'CCW Arc To'
        self._type = CommandType.CW_ARC_TO
        self._arc_type = arc_type
        self._arc_dir = arc_dir
        self._center1 = Point2()
        self._center2 = Point2()

        self._parse()

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'n={self._index} ' \
               f'x={self._x} ' \
               f'y={self._y} ' \
               f'r={self._r} ' \
               f't={self._arc_type} ' \
               f'd={self._arc_dir} ' \
               f'sp={self._speed} ' \
               f'p1={self._spill} ' \
               f'l={self.length})'

    @property
    def enabled(self):
        return range(1, 8)

    @property
    def length(self):
        return sum(p.length for p in self._geom_primitives)

    @property
    def is_move(self):
        return True

    @property
    def is_short(self):
        return len(self._cnc_lines) == 3

    @property
    def is_long(self):
        return len(self._cnc_lines) == 4

    def _parse(self):

        def parse_short():
            line3 = self._cnc_lines[-1]

            params = line3.gcodes[0].params

            self._geom_end_point = Point2(params['X'].value, params['Y'].value)

            center = Point2(params['I'].value, params['J'].value)
            self._center1 = center

            self._r = round(math.sqrt(pow(self._geom_end_point.x - center.x, 2) +
                                      pow(self._geom_end_point.y - center.y, 2)), 1)
            self._x = self._geom_end_point.x
            self._y = self._geom_end_point.y

            self._geom_primitives.append(Arc(center, self._r, self._geom_start_point, self._geom_end_point))

        def parse_long():
            *_, line3, line4 = self._cnc_lines

            params1 = line3.gcodes[0].params
            params2 = line4.gcodes[0].params

            arc1_end = Point2(params1['X'].value, params1['Y'].value)
            center1 = Point2(params1['I'].value, params1['J'].value)
            arc2_end = Point2(params2['X'].value, params2['Y'].value)
            center2 = Point2(params2['I'].value, params2['J'].value)

            self._geom_end_point = arc2_end
            self._center1 = center1
            self._center2 = center2

            self._r = round(math.sqrt(pow(self._geom_end_point.x - center1.x, 2) +
                                      pow(self._geom_end_point.y - center1.y, 2)), 1)
            self._x = self._geom_end_point.x
            self._y = self._geom_end_point.y

            self._geom_primitives.append(Arc(center1, self._r, self._geom_start_point, arc1_end))
            self._geom_primitives.append(Arc(center2, self._r, arc1_end, arc2_end))

        super()._parse()
        self._index = self._cnc_lines[0].gcodes[0].number
        self._spill = self._cnc_lines[0].block.modal_params[1].value
        self._speed = self._cnc_lines[1].gcodes[0].word.value

        if self.is_short:
            parse_short()
        elif self.is_long:
            parse_long()

    def shift(self, direction, value):
        print(self.__class__.__name__, direction, value)

        def shift_short():
            new_end_point = Point2(new_end_x, new_end_y)
            new_start_point = Point2(new_start_x, new_start_y)
            new_center1_point = Point2(new_center1_x, new_center1_y)

            self._geom_start_point = new_start_point
            self._geom_end_point = new_end_point
            self._center1 = new_center1_point

            self._x = self._geom_end_point.x
            self._y = self._geom_end_point.y

            self._geom_primitives.clear()
            self._geom_primitives.append(Arc(new_center1_point, self._r, self._geom_start_point, self._geom_end_point))

        def shift_long():
            new_end_point = Point2(new_end_x, new_end_y)
            new_start_point = Point2(new_start_x, new_start_y)
            new_center1_point = Point2(new_center1_x, new_center1_y)
            new_center2_point = Point2(new_center1_x, new_center1_y)
            new_arc1_end_point = Point2(new_arc1_end_x, new_arc1_end_y)
            new_arc2_end_point = Point2(new_arc2_end_x, new_arc2_end_y)

            self._geom_start_point = new_start_point
            self._geom_end_point = new_end_point
            self._center1 = new_center1_point
            self._center2 = new_center2_point

            self._x = self._geom_end_point.x
            self._y = self._geom_end_point.y

            self._geom_primitives.clear()
            self._geom_primitives.append(Arc(new_center1_point, self._r, self._geom_start_point, new_arc1_end_point))
            self._geom_primitives.append(Arc(new_center2_point, self._r, new_arc1_end_point, new_arc2_end_point))

        new_start_x, new_start_y = self._geom_start_point.x, self._geom_start_point.y
        new_end_x, new_end_y = self._geom_end_point.x, self._geom_end_point.y
        new_center1_x, new_center1_y = self._center1.x, self._center1.y
        new_center2_x, new_center2_y = self._center2.x, self._center2.y
        new_arc1_end_x, new_arc1_end_y = self._geom_primitives[0].p2.x, self._geom_primitives[0].p2.y

        new_arc2_end_x, new_arc2_end_y = 0, 0
        try:
            new_arc2_end_x, new_arc2_end_y = self._geom_primitives[1].p2.x, self._geom_primitives[1].p2.y
        except IndexError:
            pass

        if direction == 'right':
            new_start_x += value
            new_end_x += value
            new_center1_x += value
            new_center2_x += value
            new_arc1_end_x += value
            new_arc2_end_x += value
        elif direction == 'left':
            new_start_x -= value
            new_end_x -= value
            new_center1_x -= value
            new_center2_x -= value
            new_arc1_end_x -= value
            new_arc2_end_x -= value
        elif direction == 'up':
            new_start_y += value
            new_end_y += value
            new_center1_y += value
            new_center2_y += value
            new_arc1_end_y += value
            new_arc2_end_y += value
        elif direction == 'down':
            new_start_y -= value
            new_end_y -= value
            new_center1_y -= value
            new_center2_y -= value
            new_arc1_end_y -= value
            new_arc2_end_y -= value

        if self.is_short:
            shift_short()
        elif self.is_long:
            shift_long()


class LineToWithEndCurveCommand(Command):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Line To (e)'
        self._type = CommandType.LINE_TO_END

        self._parse()

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'n={self._index} ' \
               f'x={self._x} ' \
               f'y={self._y} ' \
               f'r={self._r} ' \
               f'sp={self._speed} ' \
               f'p1={self._spill} ' \
               f'l={self.length})'

    @property
    def enabled(self):
        return 1, 2, 3, 4, 6, 7

    @property
    def length(self):
        return sum(p.length for p in self._geom_primitives)

    @property
    def is_move(self):
        return True

    def _parse(self):
        super()._parse()
        self._index = self._cnc_lines[0].gcodes[0].number
        self._spill = self._cnc_lines[0].block.modal_params[1].value
        self._speed = self._cnc_lines[1].gcodes[0].word.value

        *_, line3, line4 = self._cnc_lines

        params1 = line3.gcodes[0].params
        params2 = line4.gcodes[0].params

        line_end = Point2(params1['X'].value, params1['Y'].value)
        arc_end = Point2(params2['X'].value, params2['Y'].value)
        arc_center = Point2(params2['I'].value, params2['J'].value)

        self._r = round(math.sqrt(pow(arc_end.x - arc_center.x, 2) +
                                  pow(arc_end.y - arc_center.y, 2)), 1)

        self._geom_end_point = arc_end
        l1 = Line2(self._geom_start_point, line_end)
        l2 = Line2(arc_center, arc_end)
        end_point = l2.intersect(l1)

        self._x = round(end_point.x, 1)
        self._y = round(end_point.y, 1)

        self._geom_primitives.append(LineSegment2(self._geom_start_point, line_end))
        self._geom_primitives.append(Arc(arc_center, self._r, line_end, arc_end))

    def shift(self, direction, value):
        print(self.__class__.__name__, direction, value)


class LineToWithStartCurveCommand(Command):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Line To (s)'
        self._type = CommandType.LINE_TO_END

        self._parse()

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'n={self._index} ' \
               f'x={self._x} ' \
               f'y={self._y} ' \
               f'r={self._r} ' \
               f'sp={self._speed} ' \
               f'p1={self._spill} ' \
               f'l={self.length})'

    def __getitem__(self, item):
        ret = super().__getitem__(item)
        if item == 4:
            ret = '*'
        return ret

    @property
    def enabled(self):
        return 1, 2, 3, 4, 6, 7

    @property
    def length(self):
        return sum(p.length for p in self._geom_primitives)

    @property
    def is_move(self):
        return True

    def _parse(self):
        super()._parse()
        self._index = self._cnc_lines[0].gcodes[0].number
        self._spill = self._cnc_lines[0].block.modal_params[1].value
        self._speed = self._cnc_lines[1].gcodes[0].word.value

        *_, line3, line4 = self._cnc_lines

        params1 = line3.gcodes[0].params
        params2 = line4.gcodes[0].params

        arc_end = Point2(params1['X'].value, params1['Y'].value)
        arc_center = Point2(params1['I'].value, params1['J'].value)
        line_end = Point2(params2['X'].value, params2['Y'].value)

        self._r = round(math.sqrt(pow(arc_end.x - arc_center.x, 2) +
                                  pow(arc_end.y - arc_center.y, 2)), 1)

        self._geom_end_point = line_end
        l2 = Line2(arc_center, self._geom_start_point)
        l1 = Line2(arc_end, line_end)
        end_point = l2.intersect(l1)

        self._x = round(line_end.x, 1)
        self._y = round(line_end.y, 1)

        self._geom_primitives.append(Arc(arc_center, self._r, self._geom_start_point, arc_end))
        self._geom_primitives.append(LineSegment2(arc_end, line_end))

    def shift(self, direction, value):
        print(self.__class__.__name__, direction, value)


class LineToWithBothCurvesCommand(Command):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Line To (b)'
        self._type = CommandType.LINE_TO_BOTH

        self._parse()

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'n={self._index} ' \
               f'x={self._x} ' \
               f'y={self._y} ' \
               f'r={self._r} ' \
               f'sp={self._speed} ' \
               f'p1={self._spill} ' \
               f'l={self.length})'

    @property
    def enabled(self):
        return 1, 2, 3, 4, 6, 7

    @property
    def length(self):
        return sum(p.length for p in self._geom_primitives)

    @property
    def is_move(self):
        return True

    def _parse(self):
        super()._parse()
        self._index = self._cnc_lines[0].gcodes[0].number
        self._spill = self._cnc_lines[0].block.modal_params[1].value
        self._speed = self._cnc_lines[1].gcodes[0].word.value

        *_, line3, line4, line5 = self._cnc_lines

        params_arc1 = line3.gcodes[0].params
        params_line = line4.gcodes[0].params
        params_arc2 = line5.gcodes[0].params

        arc1_begin = self._geom_start_point.copy()
        arc1_end = Point2(params_arc1['X'].value, params_arc1['Y'].value)
        arc1_center = Point2(params_arc1['I'].value, params_arc1['J'].value)
        arc1_rad = math.sqrt(pow(arc1_end.x - arc1_center.x, 2) + pow(arc1_end.y - arc1_center.y, 2))

        line_end = Point2(params_line['X'].value, params_line['Y'].value)

        arc2_end = Point2(params_arc2['X'].value, params_arc2['Y'].value)
        arc2_center = Point2(params_arc2['I'].value, params_arc2['J'].value)
        arc2_rad = math.sqrt(pow(arc2_end.x - arc2_center.x, 2) + pow(arc2_end.y - arc2_center.y, 2))

        l1 = Line2(arc2_center, arc2_end)
        l2 = Line2(arc1_end, line_end)
        end_point = l1.intersect(l2)

        self._x = round(end_point.x, 1)
        self._y = round(end_point.y, 1)
        self._r = round(arc2_rad, 1)

        self._geom_end_point = arc2_end.copy()

        self._geom_primitives.append(Arc(arc1_center, arc1_rad, arc1_begin, arc1_end))
        self._geom_primitives.append(LineSegment2(arc1_end, line_end))
        self._geom_primitives.append(Arc(arc2_center, arc2_rad, line_end, arc2_end))

    def shift(self, direction, value):
        print(self.__class__.__name__, direction, value)


class CNFile:
    def __init__(self, filename=None):
        self._filename = filename
        self._raw_lines = list()

        self._header = list()
        self._commands = list()
        self._footer = list()

        self._load()
        self._parse()

    def _load(self):
        if os.path.isfile(self._filename):
            with open(self._filename, mode='rt') as f:
                self._raw_lines = f.readlines()

    def _parse(self):
        command_block = ''
        for line in self._raw_lines:
            line = line.strip()
            if r'//' in line or r'%' in line or ':' in line or 'G71' in line or 'G90' in line:
                self._header.append(line)

            elif line.startswith('N'):
                if not command_block:
                    command_block = line
                    continue
                else:
                    self._commands.append(Command.from_lines(command_block, previous=None if not self._commands else self._commands[-1]))
                    command_block = line

            elif not line or 'M30' in line:
                self._footer.append(line)
                if command_block:
                    self._commands.append(Command.from_lines(command_block, previous=None if not self._commands else self._commands[-1]))
                command_block = ''

            else:
                command_block += '\n' + line

    @property
    def length(self):
        return sum(el.length for el in self._commands)
