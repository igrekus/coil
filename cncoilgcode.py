import os
import math

from enum import Enum
from euclid3 import Point2, Line2, LineSegment2, Circle
from pygcode import Line


class CnCommandType(Enum):
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
        THERM_UP,\
        LINE_TO,\
        CW_ARC_TO, \
        CCW_ARC_TO = range(19)


class ArcType(Enum):
    SHORT, LONG = range(2)


class ArcDirection(Enum):
    CW, CCW = range(2)


arc_label = {ArcType.SHORT: 'Short', ArcType.LONG: 'Long'}


class Command:
    def __init__(self, text, previous=None):
        self._text: str = text.strip()

        self._previous = previous

        self._label = ''
        self._index = 0
        self._x = 0
        self._y = 0
        self._r = 0
        self._arc = ''
        self._speed = 0
        self._spill = 0
        self._delay = 0
        self._pm = 0

        self._gcode = ''
        self._gcode_x = 0
        self._gcode_y = 0
        self._comand_type = None
        self._moves = list()

        self._parse()

    def _parse(self):
        if self._text == 'G71':
            self._gcode = 'G71'
            self._label = 'Старт'
        elif self._text == 'G90':
            self._gcode = 'G90'
            self._label = 'Абсолют'
        elif self._text == 'M30':
            self._gcode = 'M30'
            self._label = 'Конец'
        elif self._text.startswith('N'):
            ts = self._text.split('\n')
            if len(ts) == 1:
                params = ts[0].split(' ')
                self._index = int(params[0][1:4])
                self._gcode = params[1]
                self._pm = int(params[2][1:])

                gcode = params[1]
                if gcode == 'M70':
                    self._label = 'Weld'
                elif gcode == 'M71':
                    self._label = 'Sono up'
                elif gcode == 'M72':
                    self._label = 'Sono mid'
                elif gcode == 'M73':
                    self._label = 'Sono low'
                elif gcode == 'M74':
                    self._label = 'Cut wire'
                elif gcode == 'M75':
                    self._label = 'Embed on'
                elif gcode == 'M76':
                    self._label = 'Embed off'
                elif gcode == 'M77':
                    self._label = 'Pull wire'
                elif gcode == 'M78':
                    self._label = 'Hold module'
                elif gcode == 'M79':
                    self._label = 'Release module'
                elif gcode == 'M80':
                    self._label = 'Brake on'
                elif gcode == 'M81':
                    self._label = 'Brake off'
                elif gcode == 'M82':
                    self._label = 'Thermode mid'
                elif gcode == 'M83':
                    self._label = 'Thermode up'

            elif len(ts) == 2:
                line1, line2 = ts
                params = line1.split(' ')
                self._index = int(params[0][1:4])
                self._gcode = 'M501'
                self._label = 'Fill'
                self._spill = int(params[2][1:])
                self._delay = int(float(params[3][1:]) * 1000)

            elif len(ts) == 3:
                line1, line2, line3 = ts
                self._index = int(line1[1:4])
                self._spill = int(line1[11:])
                self._speed = int(line2[1:])

                gcode, *params = line3.split(' ')

                self._gcode = gcode

                self._gcode_x = self._x = float(params[0][1:])
                self._gcode_y = self._y = float(params[1][1:])
                if len(params) == 3:
                    self._label = 'Line To'
                    self._r = '*'
                elif len(params) == 6:
                    if gcode == 'G03':
                        self._label = 'CCW Arc To (s)'
                    elif gcode == 'G02':
                        self._label = 'CW Arc To (s)'
                    self._arc = 'Short'
                    i, j = float(params[3][1:]), float(params[4][1:])
                    self._r = round(math.sqrt(pow(self._x - i, 2) + pow(self._y - j, 2)), 1)

            elif len(ts) == 4:
                line1, line2, line3, line4 = ts
                self._index = int(line1[1:4])
                self._spill = int(line1[11:])
                self._speed = int(line2[1:])

                gcode1, *params1 = line3.split(' ')
                gcode2, *params2 = line4.split(' ')

                # arc + arc = arc long
                if gcode1 != 'G01' and gcode2 != 'G01':
                    if gcode1 == 'G02':
                        self._label = 'CW Arc To (l)'
                        self._gcode = 'G02'
                    elif gcode1 == 'G03':
                        self._gcode = 'G03'
                        self._label = 'CCW Arc To (l)'

                    self._arc = 'Long'

                    self._gcode_x = self._x = float(params2[0][1:])
                    self._gcode_y = self._y = float(params2[1][1:])

                    i1, j1 = float(params1[3][1:]), float(params1[4][1:])
                    r1 = round(math.sqrt(pow(float(params1[0][1:]) - i1, 2) + pow(float(params1[1][1:]) - j1, 2)), 1)
                    self._r = r1

                    # i2, j2 = float(params2[3][1:]), float(params2[4][1:])
                    # r2 = round(math.sqrt(pow(self._x - i2, 2) + pow(self._y - j2, 2)))

                # line + arc = line with end curve
                elif gcode1 == 'G01':
                    self._label = 'Line To (e)'
                    self._gcode = 'G01'

                    x1, y1 = self._previous._gcode_x, self._previous._gcode_y
                    x2, y2 = float(params1[0][1:]), float(params1[1][1:])

                    x3, y3 = float(params2[3][1:]), float(params2[4][1:])
                    x4, y4 = float(params2[0][1:]), float(params2[1][1:])

                    l1 = Line2(Point2(x1, y1), Point2(x2, y2))
                    l2 = Line2(Point2(x3, y3), Point2(x4, y4))

                    intersect: Point2 = l2.intersect(l1)

                    self._x = round(intersect.x, 1)
                    self._y = round(intersect.y, 1)
                    self._r = round(math.sqrt(pow(x4 - x3, 2) + pow(y4 - y3, 2)), 1)

                    self._gcode_x = x4
                    self._gcode_y = y4

                    # t12 = (y2 - y1) / (x2 - x1)
                    # t34 = (y4 - y3) / (x4 - x3)
                    # self._x = round((y3 - y1 + t12*x1 - t34*x3) / (t12 - t34), 1)
                    # self._y = round(y1 + t12*self._x - t12*x1, 1)

                # arc + line = line with start curve
                elif gcode2 == 'G01':
                    self._label = 'Line To (s)'
                    self._gcode = 'G01'

                    x1, y1 = self._previous._gcode_x, self._previous._gcode_y
                    x2, y2 = float(params1[3][1:]), float(params1[4][1:])

                    x3, y3 = float(params1[0][1:]), float(params1[1][1:])
                    x4, y4 = float(params2[0][1:]), float(params2[1][1:])

                    l1 = Line2(Point2(x1, y1), Point2(x2, y2))
                    l2 = Line2(Point2(x3, y3), Point2(x4, y4))

                    intersect: Point2 = l2.intersect(l1)

                    self._x = round(x4, 1)
                    self._y = round(y4, 1)
                    # self._r = round(math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2)), 1)
                    self._r = '*'

                    self._gcode_x = x4
                    self._gcode_y = y4

            elif len(ts) == 5:
                line1, line2, line3, line4, line5 = ts
                self._index = int(line1[1:4])
                self._spill = int(line1[11:])
                self._speed = int(line2[1:])

                gcode1, *params1 = line3.split(' ')
                gcode2, *params2 = line4.split(' ')
                gcode3, *params3 = line5.split(' ')

                self._label = 'Line To (b)'
                self._gcode = 'G01'

                x1, y1 = float(params1[0][1:]), float(params1[1][1:])
                x2, y2 = float(params2[0][1:]), float(params2[1][1:])

                x3, y3 = float(params3[3][1:]), float(params3[4][1:])
                x4, y4 = float(params3[0][1:]), float(params3[1][1:])

                l1 = Line2(Point2(x1, y1), Point2(x2, y2))
                l2 = Line2(Point2(x3, y3), Point2(x4, y4))

                intersect: Point2 = l2.intersect(l1)

                self._x = round(intersect.x, 1)
                self._y = round(intersect.y, 1)
                self._r = round(math.sqrt(pow(x4 - x3, 2) + pow(y4 - y3, 2)), 1)

                self._gcode_x = x4
                self._gcode_y = y4

    def __str__(self):
        return f'Command(text={self._text})'

    def __len__(self):
        if self._gcode not in ['G01', 'G02', 'G03']:
            return 0
        return 100

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
            return self._arc
        elif item == 6:
            return self._speed
        elif item == 7:
            return self._spill
        elif item == 8:
            return self._delay
        elif item == 9:
            return self._pm
        elif item == 'gcode':
            return self._gcode


class CnCommand:
    def __init__(self, text, previous=None):
        self._text: str = text
        self._lines: list = text.split('\n')

        self._type: CnCommandType = CnCommandType.UNDEFINED
        self._previous: CnCommand = previous
        self._geom_start_point: Point2 = Point2(0, 0) if not previous else self._previous._geom_end_point

        self._cnc_lines: list = list()

        self._geom_end_point: Point2 = self._geom_start_point
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

    def _parse(self):
        self._cnc_lines = [Line(l) for l in self._lines]

    @staticmethod
    def from_lines(text, previous):
        lines = text.split('\n')
        length = len(lines)
        if length == 1:
            line = lines[0]
            if 'M70' in line:
                return WeldCnCommand(text=text, previous=previous)
            elif 'M71' in line:
                return SonoUpCnCommand(text=text, previous=previous)
            elif 'M72' in line:
                return SonoMidCnCommand(text=text, previous=previous)
            elif 'M73' in line:
                return SonoLowCnCommand(text=text, previous=previous)
            elif 'M74' in line:
                return CutWireCnCommand(text=text, previous=previous)
            elif 'M75' in line:
                return EmbedOnCnCommand(text=text, previous=previous)
            elif 'M76' in line:
                return EmbedOffCnCommand(text=text, previous=previous)
            elif 'M77' in line:
                return EmbedOffCnCommand(text=text, previous=previous)
            elif 'M78' in line:
                return HoldModuleCnCommand(text=text, previous=previous)
            elif 'M79' in line:
                return ReleaseModuleCnCommand(text=text, previous=previous)
            elif 'M80' in line:
                return BrakeOnCnCommand(text=text, previous=previous)
            elif 'M81' in line:
                return BrakeOffCnCommand(text=text, previous=previous)
            elif 'M82' in line:
                return ThermMidCnCommand(text=text, previous=previous)
            elif 'M83' in line:
                return ThermUpCnCommand(text=text, previous=previous)
        elif length == 2:
            return FillCnCommand(text=text, previous=previous)
        elif length == 3:
            line1, line2, line3 = lines
            if 'G01' in line3:
                return LineToCnCommand(text=text, previous=previous)
            elif 'G02' in line3:
                return ArcToCnCommand(text=text, previous=previous, arc_type=ArcType.SHORT, arc_dir=ArcDirection.CW)
            elif 'G03' in line3:
                return ArcToCnCommand(text=text, previous=previous, arc_type=ArcType.SHORT, arc_dir=ArcDirection.CCW)
        elif length == 4:
            # long arc = arc + arc
            line1, line2, line3, line4 = lines
            if 'G01' not in line3 and 'G01' not in line4:
                if 'G02' in line3 and 'G02' in line4:
                    return ArcToCnCommand(text=text, previous=previous, arc_type=ArcType.LONG, arc_dir=ArcDirection.CW)
                elif 'G03' in line3 and 'G03' in line4:
                    return ArcToCnCommand(text=text, previous=previous, arc_type=ArcType.LONG, arc_dir=ArcDirection.CCW)

        else:
            return CnCommand(text=text, previous=previous)


class FillCnCommand(CnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Fill'
        self._type = CnCommandType.FILL

        self._parse()

    def __str__(self):
        return f'FillCnCommand(n={self._index} p1={self._spill} p2={self._delay})'

    def _parse(self):
        super()._parse()
        assert len(self._cnc_lines) == 2

        line1, line2 = self._cnc_lines
        assert line1.gcodes[0].word_letter == 'N'
        assert line2.gcodes[0].word == 'G04'

        self._index = line1.gcodes[0].number
        self._spill = line1.block.modal_params[1].value
        self._delay = line1.block.modal_params[2].value * 1000


class OneLineCnCommand(CnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'undefined one-line command'
        self._type = CnCommandType.UNDEFINED

        self._parse()

    def __str__(self):
        return f'{self.__class__.__name__}(n={self._index} prm={self._prm})'

    def _parse(self):
        super()._parse()
        assert len(self._cnc_lines) == 1

        line1 = self._cnc_lines[0]
        assert line1.gcodes[0].word_letter == 'N'

        self._index = line1.gcodes[0].number
        self._spill = self._prm = line1.block.modal_params[1].value
        self._delay = line1.block.modal_params[2].value


class WeldCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Weld'
        self._type = CnCommandType.WELD


class SonoUpCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Sono Up'
        self._type = CnCommandType.SONO_UP


class SonoMidCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Sono Mid'
        self._type = CnCommandType.SONO_MID


class SonoLowCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Sono Low'
        self._type = CnCommandType.SONO_LOW


class CutWireCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Cut wire'
        self._type = CnCommandType.CUT_WIRE


class EmbedOnCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Embed on'
        self._type = CnCommandType.EMBED_ON


class EmbedOffCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Embed off'
        self._type = CnCommandType.EMBED_OFF


class PullWireCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Pull wire'
        self._type = CnCommandType.PULL_WIRE


class HoldModuleCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Hold module'
        self._type = CnCommandType.HOLD_MODULE


class ReleaseModuleCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Release module'
        self._type = CnCommandType.RELEASE_MODULE


class BrakeOnCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Brake on'
        self._type = CnCommandType.BRAKE_ON


class BrakeOffCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Brake off'
        self._type = CnCommandType.BRAKE_OFF


class ThermMidCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Therm mid'
        self._type = CnCommandType.THERM_MID


class ThermUpCnCommand(OneLineCnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Therm up'
        self._type = CnCommandType.THERM_UP


class LineToCnCommand(CnCommand):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Line To'
        self._type = CnCommandType.LINE_TO

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
    def length(self):
        return self._geom_primitives[0].length

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


class ArcToCnCommand(CnCommand):
    def __init__(self, text, previous=None, arc_type=ArcType.SHORT, arc_dir=ArcDirection.CW):
        super().__init__(text, previous)
        self._label = 'CW Arc To' if arc_dir else 'CCW Arc To'
        self._type = CnCommandType.CW_ARC_TO
        self._arc_type = arc_type
        self._arc_dir = arc_dir

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
    def length(self):
        # TODO calc actual arc length
        return 2 * math.pi * self._geom_primitives[0].r

    def _parse(self):

        def parse_short():
            line3 = self._cnc_lines[-1]

            params = line3.gcodes[0].params

            self._geom_end_point = Point2(params['X'].value, params['Y'].value)

            center = Point2(params['I'].value, params['J'].value)

            self._r = round(math.sqrt(pow(self._geom_end_point.x - center.x, 2) +
                                      pow(self._geom_end_point.y - center.y, 2)), 1)
            self._x = self._geom_end_point.x
            self._y = self._geom_end_point.y

            # TODO create actual arc
            self._geom_primitives.append(Circle(center, self._r))

        def parse_long():
            *_, line3, line4 = self._cnc_lines

            params1 = line3.gcodes[0].params
            params2 = line4.gcodes[0].params

            self._geom_end_point = Point2(params2['X'].value, params2['Y'].value)

            arc1_end = Point2(params1['X'].value, params1['Y'].value)
            center1 = Point2(params1['I'].value, params1['J'].value)
            arc2_end = Point2(params2['X'].value, params2['Y'].value)
            center2 = Point2(params2['I'].value, params2['J'].value)

            self._r = round(math.sqrt(pow(self._geom_end_point.x - center1.x, 2) +
                                      pow(self._geom_end_point.y - center1.y, 2)), 1)
            self._x = self._geom_end_point.x
            self._y = self._geom_end_point.y

            # TODO calc actual arc
            self._geom_primitives.append(Circle(center1, self._r))
            self._geom_primitives.append(Circle(center2, self._r))

        super()._parse()
        self._index = self._cnc_lines[0].gcodes[0].number
        self._spill = self._cnc_lines[0].block.modal_params[1].value
        self._speed = self._cnc_lines[1].gcodes[0].word.value

        if len(self._cnc_lines) == 3:
            parse_short()
        elif len(self._cnc_lines) == 4:
            parse_long()


class CNFile:
    def __init__(self, filename=None):
        self._filename = filename
        self._raw_lines = list()

        self._header = list()
        self._commands = list()
        self._cncommands = list()
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
                    self._commands.append(Command(command_block, previous=None if not self._commands else self._commands[-1]))
                    self._cncommands.append(CnCommand.from_lines(command_block, previous=None if not self._cncommands else self._cncommands[-1]))
                    command_block = line

            elif not line or 'M30' in line:
                self._footer.append(line)
                if command_block:
                    self._commands.append(Command(command_block, previous=None if not self._commands else self._commands[-1]))
                    self._cncommands.append(CnCommand.from_lines(command_block, previous=None if not self._cncommands else self._cncommands[-1]))
                command_block = ''

            else:
                command_block += '\n' + line
