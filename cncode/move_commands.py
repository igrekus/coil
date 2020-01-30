from euclid3 import LineSegment2, Point2
from pygcode import Line

from cncode.bases import MoveCommand, CommandType, ArcType

# TODO cases
# - arc R == distance between points -> long arc
# - arc R < distance between points, arc == short -> short arc, R = ?
# - arc R < distance between points, arc == long -> long arc, R = ?


class LineToCommand(MoveCommand):
    def __init__(self, index: int=0, x: float=0.0, y: float=0.0, speed: float=0.0, spill: float=0.0,
                 prev_gui_end: Point2=None, prev_gcode_end: Point2=None):

        super().__init__(type_=CommandType.LINE_TO, index=index, label='Line To', x=x, y=y, speed=speed, spill=spill,
                         prev_gui_end=prev_gui_end, prev_gcode_end=prev_gcode_end)

    def __str__(self):
        return f'{self.__class__.__name__}(x={self._gui_p2.x}, y={self._gui_p2.y}, ' \
               f'speed={self._speed}, spill={self._spill})'

    def __getitem__(self, item):
        if item == 4:
            return '*'
        elif item == 5:
            return ''
        else:
            return super().__getitem__(item)

    @property
    def disabled(self):
        return 5, 8, 9

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M500 P{self._spill}\n' \
               f'     F{self._speed:.0f}\n' \
               f'     G01 X{self.gcode_end_x} Y{self.gcode_end_y} Z0\n'

    @property
    def gui_geometry(self):
        return [LineSegment2(self._gui_p1, self._gui_p2)]

    @property
    def gcode_geometry(self):
        return self.gui_geometry

    @property
    def gcode_end_x(self):
        return self.gcode_geometry[-1].p2.x

    @property
    def gcode_end_y(self):
        return self.gcode_geometry[-1].p2.y

    @property
    def length(self):
        return sum(g.length for g in self.gcode_geometry)

    @classmethod
    def from_string(cls, string: str, *args, **kwargs):
        prev_gui_end = kwargs.get('prev_gui_end', Point2())
        prev_gcode_end = kwargs.get('prev_gcode_end', Point2())
        cnc_lines = [Line(l) for l in string.strip().split('\n')]
        assert len(cnc_lines) == 3

        line1, line2, line3 = cnc_lines

        index = line1.gcodes[0].number
        spill = line1.block.modal_params[1].value
        speed = line2.gcodes[0].word.value

        params = line3.gcodes[0].params
        geom_end_point = Point2(params['X'].value, params['Y'].value)

        x = geom_end_point.x
        y = geom_end_point.y

        return cls(index=index, x=x, y=y,
                   speed=speed, spill=spill,
                   prev_gui_end=prev_gui_end,
                   prev_gcode_end=prev_gcode_end)


class LineToWithEndCurveCommand(MoveCommand):
    def __init__(self, index: int=0, x: float=0.0, y: float=0.0, speed: float=0.0, spill: float=0.0,
                 prev_gui_end: Point2=None, prev_gcode_end: Point2=None):

        super().__init__(type_=CommandType.LINE_TO_END,
                         index=index, label='Line To', x=x, y=y, speed=speed, spill=spill,
                         prev_gui_end=prev_gui_end, prev_gcode_end=prev_gcode_end)

    def __str__(self):
        return f'{self.__class__.__name__}(x={self._gui_p2.x}, y={self._gui_p2.y}, ' \
               f'r={self._r}, speed={self._speed}, spill={self._spill})'

    def __getitem__(self, item):
        if item == 5:
            return ''
        else:
            return super().__getitem__(item)

    @property
    def disabled(self):
        return 5, 8, 9

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M500 P{self._spill}\n' \
               f'     F{self._speed:.0f}\n' \
               f'     G01 X{self.gcode_end_x} Y{self.gcode_end_y} Z0\n'

    @property
    def gui_geometry(self):
        return [LineSegment2(self._gui_p1, self._gui_p2)]

    @property
    def gcode_geometry(self):
        print(self._gui_p1)
        print(self._gui_p2)
        return self.gui_geometry

    @property
    def gcode_end_x(self):
        return self.gcode_geometry[-1].p2.x

    @property
    def gcode_end_y(self):
        return self.gcode_geometry[-1].p2.y

    @property
    def length(self):
        return sum(g.length for g in self.gcode_geometry)

    @classmethod
    def from_string(cls, string: str, *args, **kwargs):
        prev_gui_end = kwargs.get('prev_gui_end', Point2())
        prev_gcode_end = kwargs.get('prev_gcode_end', Point2())
        cnc_lines = [Line(l) for l in string.strip().split('\n')]
        assert len(cnc_lines) == 3

        line1, line2, line3 = cnc_lines

        index = line1.gcodes[0].number
        spill = line1.block.modal_params[1].value
        speed = line2.gcodes[0].word.value

        params = line3.gcodes[0].params
        geom_end_point = Point2(params['X'].value, params['Y'].value)

        x = geom_end_point.x
        y = geom_end_point.y

        return cls(index=index, x=x, y=y,
                   speed=speed, spill=spill,
                   prev_gui_end=prev_gui_end,
                   prev_gcode_end=prev_gcode_end)


class CwShortArcToCommand(MoveCommand):
    def __init__(self, index: int=0, x: float=0.0, y: float=0.0, speed: float=0.0, spill: float=0.0,
                 prev_gui_end: Point2=None, prev_gcode_end: Point2=None):

        super().__init__(type_=CommandType.LINE_TO_END,
                         index=index, label='Line To', x=x, y=y, speed=speed, spill=spill,
                         prev_gui_end=prev_gui_end, prev_gcode_end=prev_gcode_end)

    def __str__(self):
        return f'{self.__class__.__name__}(x={self._gui_p2.x}, y={self._gui_p2.y}, ' \
               f'r={self._r}, speed={self._speed}, spill={self._spill})'

    def __getitem__(self, item):
        if item == 5:
            return ''
        else:
            return super().__getitem__(item)

    @property
    def disabled(self):
        return 5, 8, 9

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M500 P{self._spill}\n' \
               f'     F{self._speed:.0f}\n' \
               f'     G01 X{self.gcode_end_x} Y{self.gcode_end_y} Z0\n'

    @property
    def gui_geometry(self):
        return [LineSegment2(self._gui_p1, self._gui_p2)]

    @property
    def gcode_geometry(self):
        print(self._gui_p1)
        print(self._gui_p2)
        return self.gui_geometry

    @property
    def gcode_end_x(self):
        return self.gcode_geometry[-1].p2.x

    @property
    def gcode_end_y(self):
        return self.gcode_geometry[-1].p2.y

    @property
    def length(self):
        return sum(g.length for g in self.gcode_geometry)

    @classmethod
    def from_string(cls, string: str, *args, **kwargs):
        prev_gui_end = kwargs.get('prev_gui_end', Point2())
        prev_gcode_end = kwargs.get('prev_gcode_end', Point2())
        cnc_lines = [Line(l) for l in string.strip().split('\n')]
        assert len(cnc_lines) == 3

        line1, line2, line3 = cnc_lines

        index = line1.gcodes[0].number
        spill = line1.block.modal_params[1].value
        speed = line2.gcodes[0].word.value

        params = line3.gcodes[0].params
        geom_end_point = Point2(params['X'].value, params['Y'].value)

        x = geom_end_point.x
        y = geom_end_point.y

        return cls(index=index, x=x, y=y,
                   speed=speed, spill=spill,
                   prev_gui_end=prev_gui_end,
                   prev_gcode_end=prev_gcode_end)
