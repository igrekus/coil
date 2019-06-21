import datetime
import os
from math import sqrt

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsView, QGraphicsRectItem, QGraphicsScene
from pygcode import Line, GCodeMotion, GCodeLinearMove, GCodeArcMoveCW


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

        self.parse_cnc()
        self._draw()


    def parse_cnc(self):
        filename = 'vteslin.cnc'
        # filename = 'vmedved.cnc'
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

    def _draw(self):
        self.scene.addRect(0, 0, 2, 2)

        lens = list()
        x0, y0, = 0, 0
        for path in self._cnc_paths:
            zoom = 10
            params = path.block.gcodes[0].get_param_dict()
            x1, y1 = params['X'] * zoom, params['Y'] * zoom
            # if isinstance(path.block.gcodes[0], GCodeLinearMove):
            self.scene.addLine(x0, y0, x1, y1)
            lens.append(sqrt(pow(x1 - x0, 2) + pow(y1 - y0, 2)))
            x0, y0 = x1, y1

        print(sum(lens))
