import datetime
import os
from math import sqrt

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsView, QGraphicsRectItem, QGraphicsScene, \
    QGraphicsLineItem, QGraphicsEllipseItem
from pygcode import Line, GCodeMotion, GCodeLinearMove, GCodeArcMoveCW, GCodeArcMoveCCW

import euclid3


zoom = 10


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
    def __init__(self, x0, y0, x1, y1, i, j):
        super().__init__()
        self._center = euclid3.Point2(i, j)
        self._radius = sqrt(pow(x1 - i, 2) + pow(y1 - j, 2)) * zoom
        self._circle = euclid3.Circle(self._center, self._radius)

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
        filename = './gcode/output_0002.ngc'
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
            x1, y1 = params['X'], -params['Y']
            if isinstance(path.block.gcodes[0], GCodeLinearMove):
                self._geometry.append(LineSegmentItem(x0, y0, x1, y1))
            elif isinstance(path.block.gcodes[0], GCodeArcMoveCW) or isinstance(path.block.gcodes[0], GCodeArcMoveCCW):
                if 'I' not in params or 'J' not in params:
                    continue
                self._geometry.append(ArcItem(x0, y0, x1, y1, params['I'], -params['J']))
            x0, y0 = x1, y1

    def _draw(self):
        self.scene.addRect(0, 0, 2, 2)

        # https://buildmedia.readthedocs.org/media/pdf/euclid/latest/euclid.pdf   -   geometry lib
        # https://stackoverflow.com/questions/11331854/how-can-i-generate-an-arc-in-numpy
        # http://pycam.sourceforge.net/
        for line in self._geometry:
                self.scene.addItem(line)

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
