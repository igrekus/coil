import os
import math

from euclid3 import Point2, Line2


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


class CNCommand:

    def __init__(self):
        self._index: int = 0


class CNFile:
    def __init__(self, filename=None):
        self._filename = filename
        self._raw_lines = list()

        self._header = list()
        self._commands = list()

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
            if r'//' in line or r'%' in line or ':' in line or not line:
                self._header.append(line)

            elif line.startswith('N'):
                if not command_block:
                    command_block = line
                    continue
                else:
                    self._commands.append(Command(command_block, previous=self._commands[-1]))
                    command_block = line
            elif 'G71' in line or 'G90' in line or 'M30' in line:
                if command_block:
                    self._commands.append(Command(command_block, previous=self._commands[-1]))
                    command_block = ''
                self._commands.append(Command(line))
                continue
            else:
                command_block += '\n' + line
