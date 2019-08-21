import datetime
import os
import numpy
import euclid3

from numpy import arccos, cos, sin, sqrt, arcsin, arctan2

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsView, QGraphicsRectItem, QGraphicsScene, \
    QGraphicsLineItem, QGraphicsEllipseItem

from pygcode import Line, GCodeMotion, GCodeLinearMove, GCodeArcMoveCW, GCodeArcMoveCCW


zoom = 20


class LineSegmentItem(QGraphicsLineItem):

    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self._segment = euclid3.LineSegment2(euclid3.Point2(x1, y1), euclid3.Point2(x2, y2))

        self.setLine(x1 * zoom, y1 * zoom, x2 * zoom, y2 * zoom)

    @property
    def length(self):
        return sqrt(
            pow(self._segment.p2.x - self._segment.p1.x, 2) +
            pow(self._segment.p2.y - self._segment.p1.y, 2)
        )


class ArcItem(QGraphicsEllipseItem):
    def __init__(self, x0, y0, x1, y1, i, j, cw):
        super().__init__()
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.i = i
        self.j = j
        self.cw = cw
        self._center = euclid3.Point2(i, j)
        self._radius = float(sqrt(pow(x1 - i, 2) + pow(y1 - j, 2))) * zoom

        self._circle = euclid3.Circle(euclid3.Point2(i, j), self._radius)

        self._num_segments = 10
        self._segments = list()

        self.setRect(i * zoom - self._radius, j * zoom - self._radius, self._radius * 2, self._radius * 2)

    @property
    def length(self):
        return 2 * 3.1415 * self._circle.r


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi("mainwindow.ui", self)
        self.scene = QGraphicsScene()
        self._ui.viewport.setScene(self.scene)

        self._cnc = list()
        self._geometry = list()

        self.parse_cnc()
        self._build_geometry()
        self._draw()
        print(self._coil_length())

    def parse_cnc(self):
        # filename = './gcode/output_0002.ngc'
        filename = 'gcode/VTESLIN.CNC'
        with open(filename, 'rt') as f:
            for text_line in f.readlines():
                text_line.replace(r'\\', '#')
                line = Line(text_line)
                try:
                    code = line.block.gcodes[0]
                    if isinstance(code, GCodeMotion):
                        print('move', line.block.gcodes)
                        self._cnc.append(line)
                except LookupError:
                    pass

    def _build_geometry(self):
        x0, y0, = 0, 0
        for path in self._cnc:
            params = path.block.gcodes[0].get_param_dict()
            if 'X' not in params or 'Y' not in params:
                continue
            x1, y1 = params['X'], params['Y']
            if isinstance(path.block.gcodes[0], GCodeLinearMove):
                self._geometry.append(LineSegmentItem(x0, y0, x1, y1))
            elif isinstance(path.block.gcodes[0], GCodeArcMoveCW) or isinstance(path.block.gcodes[0], GCodeArcMoveCCW):
                if 'I' not in params or 'J' not in params:
                    continue
                cw = isinstance(path.block.gcodes[0], GCodeArcMoveCW)
                i, j = params['I'], params['J']
                self._geometry.append(ArcItem(x0, y0, x1, y1, i, j, cw))
            x0, y0 = x1, y1

    def _draw(self):
        self.scene.addRect(0, 0, 2, 2)

        # https://buildmedia.readthedocs.org/media/pdf/euclid/latest/euclid.pdf   -   geometry lib
        # https://stackoverflow.com/questions/11331854/how-can-i-generate-an-arc-in-numpy
        # http://pycam.sourceforge.net/

        def inv_parametric_circle(x, xc, r):
            t = arccos((x - xc) / r)
            return t

        def parametric_circle(ts, xc, yc, R):
            for t in ts:
                x, y = xc + R * cos(t), yc + R * sin(t)
                yield x, y

        steps = 10

        for line in self._geometry:
            self.scene.addItem(line)
            if isinstance(line, ArcItem):
                if line.cw:
                    arc = line

                    # 1 quadrant
                    angle_start = arctan2((arc.y0 - arc.j), (arc.x0 - arc.i))
                    angle_end = arctan2((arc.y1 - arc.j), (arc.x1 - arc.i))
                    print(angle_start, angle_end)

                    # ---------
                    r = arc._radius
                    center_x = arc._center.x * zoom
                    center_y = arc._center.y * zoom

                    start_point = (center_x + r * cos(angle_start), center_y + r * sin(angle_start))
                    end_point = (center_x + r * cos(angle_end), center_y + r * sin(angle_end))

                    start_t = inv_parametric_circle(start_point[0], center_x, r)
                    end_t = inv_parametric_circle(end_point[0], center_x, r)
                    arc_T = numpy.linspace(start_t, end_t, steps)

                    for x, y in parametric_circle(arc_T, center_x, center_y, r):
                        self.scene.addRect(x, y, 2, 2)

    def _coil_length(self):
        return sum([line.length for line in self._geometry])


a = {"title": "cnc arc", "date": "28/6/2019", "tabs": [{"title": "gcode g2 - Поиск в Google",
                                                        "url": "https://www.google.com/search?q=gcode+g2&oq=gcode+g2&aqs=chrome..69i57j69i60j0l4.12591j0j7&sourceid=chrome&ie=UTF-8",
                                                        "win": "1090"},
                                                       {"title": "CNC G Code: G02 and G03 – ManufacturingET.org",
                                                        "url": "http://www.manufacturinget.org/2011/12/cnc-g-code-g02-and-g03/",
                                                        "win": "1090"}, {
                                                           "title": "Quick G-Code Arc Tutorial: Make G02 & G03 Easy, Avoid Mistakes",
                                                           "url": "https://www.cnccookbook.com/cnc-g-code-arc-circle-g02-g03/",
                                                           "win": "1090"}, {"title": "G-коды — Энциклопедия ТриДэшника",
                                                                            "url": "https://3deshnik.ru/wiki/index.php/G-%D0%BA%D0%BE%D0%B4%D1%8B",
                                                                            "win": "1090"},
                                                       {"title": "Круговая интерполяция – G02 и G03",
                                                        "url": "http://planetacam.ru/college/learn/6-3/",
                                                        "win": "1090"}, {
                                                           "title": "G-code.Описание.Программирование окружности.Команды G02 и G03",
                                                           "url": "http://www.intuwiz.ru/articles/g02-g03.html#.XRYE3BYza3A",
                                                           "win": "1090"}, {"title": "G-code.Описание.Команда G02",
                                                                            "url": "http://www.intuwiz.ru/articles/g02.html#.XRYVTxYza3A",
                                                                            "win": "1090"}], "created": 1561731977216}
