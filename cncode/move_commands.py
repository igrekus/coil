import math

from euclid3 import LineSegment2, Point2, Circle, Ray2, Line2, Vector2
from pygcode import Line

from cncode.bases import MoveCommand, CommandType, ArcType

# TODO cases
# - arc R == distance between points -> long arc
# - arc R < distance between points, arc == short -> short arc, R = ?
# - arc R < distance between points, arc == long -> long arc, R = ?


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
    def __init__(self, index: int=0, x: float=0.0, y: float=0.0, r: float=0.0, speed: float=0.0, spill: float=0.0,
                 prev_gui_end: Point2=None, prev_gcode_end: Point2=None):

        super().__init__(type_=CommandType.LINE_TO_END,
                         index=index, label='Line To', x=x, y=y, r=r, speed=speed, spill=spill,
                         prev_gui_end=prev_gui_end, prev_gcode_end=prev_gcode_end)
        self.next_segment = Line2(self._gui_p2, Point2(x, y - 1.0))

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
        gui_line = self.gui_geometry[-1]
        next_line = self.next_segment
        arc_command = 'G03' if is_left(gui_line, next_line.p2) else 'G02'

        u: Vector2 = gui_line.v
        v: Vector2 = next_line.v

        bx = u.x / u.magnitude() + v.x / v.magnitude()
        by = u.y / u.magnitude() + v.y / v.magnitude()

        b = Vector2(bx, by)
        b_line = Line2(gui_line.p2, -b)

        print(b)
        print(b_line)

        return self.gui_geometry

    @property
    def gcode_end_x(self):
        return self.gcode_geometry[-1].p2.x

    @property
    def gcode_end_y(self):
        return self.gcode_geometry[-1].p2.y

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
    def __init__(self, index: int=0, x: float=0.0, y: float=0.0, r: float=0.0, speed: float=0.0, spill: float=0.0,
                 prev_gui_end: Point2=None, prev_gcode_end: Point2=None):

        super().__init__(type_=CommandType.CW_ARC_TO_SHORT,
                         index=index, label='CW Arc To', x=x, y=y, r=r, speed=speed, spill=spill, arc=ArcType.SHORT,
                         prev_gui_end=prev_gui_end, prev_gcode_end=prev_gcode_end)

    def __str__(self):
        return f'{self.__class__.__name__}(x={self._gui_p2.x}, y={self._gui_p2.y}, ' \
               f'r={self._r}, arc={self._arc}, speed={self._speed}, spill={self._spill})'

    @property
    def disabled(self):
        return 8, 9

    @property
    def as_gcode(self):
        center = self.gcode_geometry[-1].c
        return f'N{self._index:03d} M500 P{self._spill}\n' \
               f'     F{self._speed:.0f}\n' \
               f'     G02 X{self.gcode_end_x:.03f} Y{self.gcode_end_y:.03f} Z0 I{center.x:.03f} J{center.y:.03f} K0\n'

    @property
    def gui_geometry(self):
        x1, y1 = self._gui_p1.x, self._gui_p1.y
        x2, y2 = self._gui_p2.x, self._gui_p2.y
        R = self._r

        x3 = (x1 + x2) / 2
        y3 = (y1 + y2) / 2

        d = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
        a = d / 2
        h = math.sqrt(R * R - a * a)

        x41 = x3 + (h / d) * (y2 - y1)
        y41 = y3 - (h / d) * (x2 - x1)

        return [Arc(Point2(x41, y41), self._r, self._gui_p1, self._gui_p2)]

    @property
    def gcode_geometry(self):
        return self.gui_geometry

    @property
    def gcode_end_x(self):
        return self.gcode_geometry[-1].p2.x

    @property
    def gcode_end_y(self):
        return self.gcode_geometry[-1].p2.y

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
        geom_end_point = Point2(float(params['X'].value), float(params['Y'].value))
        center_point = Point2(float(params['I'].value), float(params['J'].value))

        x = geom_end_point.x
        y = geom_end_point.y

        r = math.sqrt(pow(geom_end_point.x - center_point.x, 2) +
                      pow(geom_end_point.y - center_point.y, 2))

        return cls(index=index, x=x, y=y, r=r, speed=speed, spill=spill,
                   prev_gui_end=prev_gui_end,
                   prev_gcode_end=prev_gcode_end)


class CcwShortArcToCommand(MoveCommand):
    def __init__(self, index: int=0, x: float=0.0, y: float=0.0, r: float=0.0, speed: float=0.0, spill: float=0.0,
                 prev_gui_end: Point2=None, prev_gcode_end: Point2=None):

        super().__init__(type_=CommandType.CCW_ARC_TO_SHORT,
                         index=index, label='CCW Arc To', x=x, y=y, r=r, speed=speed, spill=spill, arc=ArcType.SHORT,
                         prev_gui_end=prev_gui_end, prev_gcode_end=prev_gcode_end)

    def __str__(self):
        return f'{self.__class__.__name__}(x={self._gui_p2.x}, y={self._gui_p2.y}, ' \
               f'r={self._r}, arc={self._arc}, speed={self._speed}, spill={self._spill})'

    @property
    def disabled(self):
        return 8, 9

    @property
    def as_gcode(self):
        center = self.gcode_geometry[-1].c
        return f'N{self._index:03d} M500 P{self._spill}\n' \
               f'     F{self._speed:.0f}\n' \
               f'     G03 X{self.gcode_end_x:.03f} Y{self.gcode_end_y:.03f} Z0 I{center.x:.03f} J{center.y:.03f} K0\n'

    @property
    def gui_geometry(self):
        x1, y1 = self._gui_p1.x, self._gui_p1.y
        x2, y2 = self._gui_p2.x, self._gui_p2.y
        R = self._r

        x3 = (x1 + x2) / 2
        y3 = (y1 + y2) / 2

        d = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
        a = d / 2
        h = math.sqrt(R * R - a * a)

        x4 = x3 - (h / d) * (y2 - y1)
        y4 = y3 + (h / d) * (x2 - x1)

        return [Arc(Point2(x4, y4), self._r, self._gui_p1, self._gui_p2)]

    @property
    def gcode_geometry(self):
        return self.gui_geometry

    @property
    def gcode_end_x(self):
        return self.gcode_geometry[-1].p2.x

    @property
    def gcode_end_y(self):
        return self.gcode_geometry[-1].p2.y

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
        geom_end_point = Point2(float(params['X'].value), float(params['Y'].value))
        center_point = Point2(float(params['I'].value), float(params['J'].value))

        x = geom_end_point.x
        y = geom_end_point.y

        r = math.sqrt(pow(geom_end_point.x - center_point.x, 2) +
                      pow(geom_end_point.y - center_point.y, 2))

        return cls(index=index, x=x, y=y, r=r, speed=speed, spill=spill,
                   prev_gui_end=prev_gui_end,
                   prev_gcode_end=prev_gcode_end)


class CwLongArcToCommand(MoveCommand):
    def __init__(self, index: int=0, x: float=0.0, y: float=0.0, r: float=0.0, speed: float=0.0, spill: float=0.0,
                 prev_gui_end: Point2=None, prev_gcode_end: Point2=None):

        super().__init__(type_=CommandType.CW_ARC_TO_LONG,
                         index=index, label='CW Arc To', x=x, y=y, r=r, speed=speed, spill=spill, arc=ArcType.LONG,
                         prev_gui_end=prev_gui_end, prev_gcode_end=prev_gcode_end)

    def __str__(self):
        return f'{self.__class__.__name__}(x={self._gui_p2.x}, y={self._gui_p2.y}, ' \
               f'r={self._r}, arc={self._arc}, speed={self._speed}, spill={self._spill})'

    @property
    def disabled(self):
        return 8, 9

    @property
    def as_gcode(self):
        arc1, arc2 = self.gcode_geometry
        return f'N{self._index:03d} M500 P{self._spill}\n' \
               f'     F{self._speed:.0f}\n' \
               f'     G02 X{arc1.p2.x:.03f} Y{arc1.p2.y:.03f} Z0 I{arc1.c.x:.03f} J{arc1.c.y:.03f} K0\n' \
               f'     G02 X{arc2.p2.x:.03f} Y{arc2.p2.y:.03f} Z0 I{arc2.c.x:.03f} J{arc2.c.y:.03f} K0\n' \

    @property
    def gui_geometry(self):
        x1, y1 = self._gui_p1.x, self._gui_p1.y
        x2, y2 = self._gui_p2.x, self._gui_p2.y
        r = self._r

        xmid = (x1 + x2) / 2
        ymid = (y1 + y2) / 2

        d = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
        a = d / 2
        h = math.sqrt(r * r - a * a)

        xcenter = xmid - (h / d) * (y2 - y1)
        ycenter = ymid + (h / d) * (x2 - x1)

        circle = Circle(Point2(xcenter, ycenter), r)
        ray = Ray2(Point2(xmid, ymid), Point2(xcenter, ycenter))

        arc_split_point = circle.intersect(ray).p1

        return [
            Arc(Point2(xcenter, ycenter), self._r, self._gui_p1, arc_split_point),
            Arc(Point2(xcenter, ycenter), self._r, arc_split_point, self._gui_p2)
        ]

    @property
    def gcode_geometry(self):
        return self.gui_geometry

    @property
    def gcode_end_x(self):
        return self.gcode_geometry[-1].p2.x

    @property
    def gcode_end_y(self):
        return self.gcode_geometry[-1].p2.y

    @classmethod
    def from_string(cls, string: str, *args, **kwargs):
        prev_gui_end = kwargs.get('prev_gui_end', Point2())
        prev_gcode_end = kwargs.get('prev_gcode_end', Point2())
        cnc_lines = [Line(l) for l in string.strip().split('\n')]
        assert len(cnc_lines) == 4

        line1, line2, line3, line4 = cnc_lines

        index = line1.gcodes[0].number
        spill = line1.block.modal_params[1].value
        speed = line2.gcodes[0].word.value

        params1 = line3.gcodes[0].params
        params2 = line4.gcodes[0].params

        arc1_end = Point2(float(params1['X'].value), float(params1['Y'].value))
        arc1_center = Point2(float(params1['I'].value), float(params1['J'].value))
        arc2_end = Point2(float(params2['X'].value), float(params2['Y'].value))
        arc2_center = Point2(float(params2['I'].value), float(params2['J'].value))

        geom_end_point = arc2_end
        r = math.sqrt(pow(geom_end_point.x - arc1_center.x, 2) +
                      pow(geom_end_point.y - arc1_center.y, 2))

        x = geom_end_point.x
        y = geom_end_point.y

        return cls(index=index, x=x, y=y, r=r, speed=speed, spill=spill,
                   prev_gui_end=prev_gui_end,
                   prev_gcode_end=prev_gcode_end)


class CcwLongArcToCommand(MoveCommand):
    def __init__(self, index: int=0, x: float=0.0, y: float=0.0, r: float=0.0, speed: float=0.0, spill: float=0.0,
                 prev_gui_end: Point2=None, prev_gcode_end: Point2=None):

        super().__init__(type_=CommandType.CW_ARC_TO_LONG,
                         index=index, label='CCW Arc To', x=x, y=y, r=r, speed=speed, spill=spill, arc=ArcType.LONG,
                         prev_gui_end=prev_gui_end, prev_gcode_end=prev_gcode_end)

    def __str__(self):
        return f'{self.__class__.__name__}(x={self._gui_p2.x}, y={self._gui_p2.y}, ' \
               f'r={self._r}, arc={self._arc}, speed={self._speed}, spill={self._spill})'

    @property
    def disabled(self):
        return 8, 9

    @property
    def as_gcode(self):
        arc1, arc2 = self.gcode_geometry
        return f'N{self._index:03d} M500 P{self._spill}\n' \
               f'     F{self._speed:.0f}\n' \
               f'     G03 X{arc1.p2.x:.03f} Y{arc1.p2.y:.03f} Z0 I{arc1.c.x:.03f} J{arc1.c.y:.03f} K0\n' \
               f'     G03 X{arc2.p2.x:.03f} Y{arc2.p2.y:.03f} Z0 I{arc2.c.x:.03f} J{arc2.c.y:.03f} K0\n' \

    @property
    def gui_geometry(self):
        x1, y1 = self._gui_p1.x, self._gui_p1.y
        x2, y2 = self._gui_p2.x, self._gui_p2.y
        r = self._r

        xmid = (x1 + x2) / 2
        ymid = (y1 + y2) / 2

        d = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
        a = d / 2
        h = math.sqrt(r * r - a * a)

        xcenter = xmid + (h / d) * (y2 - y1)
        ycenter = ymid - (h / d) * (x2 - x1)

        circle = Circle(Point2(xcenter, ycenter), r)
        ray = Ray2(Point2(xmid, ymid), Point2(xcenter, ycenter))

        arc_split_point = circle.intersect(ray).p1

        return [
            Arc(Point2(xcenter, ycenter), self._r, self._gui_p1, arc_split_point),
            Arc(Point2(xcenter, ycenter), self._r, arc_split_point, self._gui_p2)
        ]

    @property
    def gcode_geometry(self):
        return self.gui_geometry

    @property
    def gcode_end_x(self):
        return self.gcode_geometry[-1].p2.x

    @property
    def gcode_end_y(self):
        return self.gcode_geometry[-1].p2.y

    @classmethod
    def from_string(cls, string: str, *args, **kwargs):
        prev_gui_end = kwargs.get('prev_gui_end', Point2())
        prev_gcode_end = kwargs.get('prev_gcode_end', Point2())
        cnc_lines = [Line(l) for l in string.strip().split('\n')]
        assert len(cnc_lines) == 4

        line1, line2, line3, line4 = cnc_lines

        index = line1.gcodes[0].number
        spill = line1.block.modal_params[1].value
        speed = line2.gcodes[0].word.value

        params1 = line3.gcodes[0].params
        params2 = line4.gcodes[0].params

        arc1_end = Point2(float(params1['X'].value), float(params1['Y'].value))
        arc1_center = Point2(float(params1['I'].value), float(params1['J'].value))
        arc2_end = Point2(float(params2['X'].value), float(params2['Y'].value))
        arc2_center = Point2(float(params2['I'].value), float(params2['J'].value))

        geom_end_point = arc2_end
        r = math.sqrt(pow(geom_end_point.x - arc1_center.x, 2) +
                      pow(geom_end_point.y - arc1_center.y, 2))

        x = geom_end_point.x
        y = geom_end_point.y

        return cls(index=index, x=x, y=y, r=r, speed=speed, spill=spill,
                   prev_gui_end=prev_gui_end,
                   prev_gcode_end=prev_gcode_end)


def is_left(line, c: Point2):
    return ((line.p2.x - line.p1.x) * (c.y - line.p1.y) - (line.p2.y - line.p1.y) * (c.x - line.p1.x)) > 0
