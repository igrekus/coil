import datetime
import os
from math import sqrt

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsView, QGraphicsRectItem, QGraphicsScene
from pygcode import Line, GCodeMotion, GCodeLinearMove, GCodeArcMoveCW

import euclid3


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi("mainwindow.ui", self)
        self.scene = QGraphicsScene()
        self._ui.viewport.setScene(self.scene)

        self._cnc_paths = list()
        self._geometry = list()

        self.parse_cnc()
        self._build_geometry()
        self._draw()

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
                        self._cnc_paths.append(line)
                except LookupError:
                    pass

    def _build_geometry(self):
        x0, y0, = 0, 0
        for path in self._cnc_paths:
            params = path.block.gcodes[0].get_param_dict()
            if 'X' not in params or 'Y' not in params:
                continue
            x1, y1 = params['X'], -params['Y']
            if isinstance(path.block.gcodes[0], GCodeLinearMove):
                self._geometry.append(euclid3.Line2(euclid3.Point2(x0, y0), euclid3.Point2(x1, y1)))
            elif isinstance(path.block.gcodes[0], GCodeArcMoveCW):
                if 'I' not in params or 'J' not in params:
                    continue
                i, j = params['I'], -params['J']
                center_x = i
                center_y = j
                self._geometry.append(euclid3.Circle(
                    euclid3.Point2(center_x, center_y),
                    sqrt(pow(x1 - i, 2) + pow(y1 - j, 2))
                ))
            else:
                if 'I' not in params or 'J' not in params:
                    continue
                i, j = params['I'], -params['J']
                center_x = i
                center_y = j
                self._geometry.append(euclid3.Circle(
                    euclid3.Point2(center_x, center_y),
                    sqrt(pow(x1 - i, 2) + pow(y1 - j, 2))
                ))
            x0, y0 = x1, y1

    def _draw(self):
        self.scene.addRect(0, 0, 2, 2)

        # https://buildmedia.readthedocs.org/media/pdf/euclid/latest/euclid.pdf   -   geometry lib
        # https://stackoverflow.com/questions/11331854/how-can-i-generate-an-arc-in-numpy
        # http://pycam.sourceforge.net/
        zoom = 10
        for line in self._geometry:
            if isinstance(line, euclid3.Line2):
                self.scene.addLine(line.p1.x * zoom, line.p1.y * zoom, line.p2.x * zoom, line.p2.y * zoom)
            elif isinstance(line, euclid3.Circle):
                self.scene.addRect(line.c.x * zoom, line.c.y * zoom, 2, 2)
                r = line.r * zoom
                self.scene.addEllipse(line.c.x * zoom - r, line.c.y * zoom - r, r * 2, r * 2)

    def _coil_length(self):
        return sum([

            for line in self._geometry

# http://pycam.sourceforge.net/

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
