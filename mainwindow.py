import math
import os
from copy import deepcopy

import numpy
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog

from gcodemodel import GcodeModel


class CoilParams:
    def __init__(self, gap, diam, dielec, magnet, length):
        self.wire_gap = gap
        self.wire_diameter = diam
        self.dielectric_const = dielec
        self.magnetic_const = magnet
        self.length = length

    def __str__(self):
        return f'CoilParams(' \
               f'g={self.wire_gap}' \
               f' d={self.wire_diameter}' \
               f' eps={self.dielectric_const}' \
               f' mag={self.magnetic_const}' \
               f' len={self.length})'


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi("mainwindow.ui", self)

        self.sceneGcode = QGraphicsScene()
        self._ui.viewGcode.setScene(self.sceneGcode)

        self._cnc = list()
        self._geometry = list()

        self._gcodeModel = GcodeModel(parent=self)
        self._ui.tableGcode.setModel(self._gcodeModel)
        self._currentDir = '.'

        self._init()

    def _init(self):
        self._ui.editGcodeFile.setText(self._gcodeModel.currentFile)
        self._ui.tableGcode.resizeColumnsToContents()

    def _openCNFile(self, name):
        self._currentDir = os.path.dirname(name)

        self._gcodeModel.loadDesign(name)
        self._ui.editGcodeFile.setText(os.path.normpath(name))
        self._ui.editLength.setText(str(self._gcodeModel.length))

        self.sceneGcode.clear()
        for item in self._gcodeModel.viewItems:
            self.sceneGcode.addItem(item)

    def _importJSCut(self, name):
        print(name)

    def _getFileName(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self,
                                                  caption='Открыть дизайн...',
                                                  directory=self._currentDir,
                                                  filter='CNCoil design (*.cnc);;GCode program (*.gcode)')
        return filename


    @pyqtSlot()
    def on_btnOpenGcodeFile_clicked(self):
        fn = self._getFileName()
        if fn:
            self._openCNFile(fn)

    @pyqtSlot()
    def on_btnImport_clicked(self):
        fn = self._getFileName()
        if fn:
            self._importJSCut(fn)

    @pyqtSlot()
    def on_btnCalc_clicked(self):
        coil = CoilParams(
            gap=self._ui.spinWireGap.value(),
            diam=self._ui.spinWireDiameter.value(),
            dielec=self._ui.spinDielectricConst.value(),
            magnet=self._ui.spinMagneticConst.value(),
            length=self._gcodeModel.length
        )

        self._calcElectricParams(coil)

    def _calcElectricParams(self, coil):

        capacitance = (math.pi * coil.dielectric_const * coil.length) / \
            math.log1p((coil.wire_gap - coil.wire_diameter) / coil.wire_diameter)

        inductance = ((coil.magnetic_const * coil.length) / math.pi) * \
            math.log1p((coil.wire_gap / 2) / (coil.wire_diameter / 2))

        freq = 1 / (2 * math.pi * math.sqrt(inductance * capacitance))

        self._ui.editLength.setText(f'{coil.length:.2f} мм')
        self._ui.editCapacitance.setText(f'{capacitance:.2f} пФ')
        self._ui.editInductance.setText(f'{inductance:.2f} мГн')
        self._ui.editFreq.setText(f'{freq * 100_000:.2f} мГц')


# a = {"title": "cnc arc", "date": "28/6/2019", "tabs": [{"title": "gcode g2 - Поиск в Google",
#                                                         "url": "https://www.google.com/search?q=gcode+g2&oq=gcode+g2&aqs=chrome..69i57j69i60j0l4.12591j0j7&sourceid=chrome&ie=UTF-8",
#                                                         "win": "1090"},
#                                                        {"title": "CNC G Code: G02 and G03 – ManufacturingET.org",
#                                                         "url": "http://www.manufacturinget.org/2011/12/cnc-g-code-g02-and-g03/",
#                                                         "win": "1090"}, {
#                                                            "title": "Quick G-Code Arc Tutorial: Make G02 & G03 Easy, Avoid Mistakes",
#                                                            "url": "https://www.cnccookbook.com/cnc-g-code-arc-circle-g02-g03/",
#                                                            "win": "1090"}, {"title": "G-коды — Энциклопедия ТриДэшника",
#                                                                             "url": "https://3deshnik.ru/wiki/index.php/G-%D0%BA%D0%BE%D0%B4%D1%8B",
#                                                                             "win": "1090"},
#                                                        {"title": "Круговая интерполяция – G02 и G03",
#                                                         "url": "http://planetacam.ru/college/learn/6-3/",
#                                                         "win": "1090"}, {
#                                                            "title": "G-code.Описание.Программирование окружности.Команды G02 и G03",
#                                                            "url": "http://www.intuwiz.ru/articles/g02-g03.html#.XRYE3BYza3A",
#                                                            "win": "1090"}, {"title": "G-code.Описание.Команда G02",
#                                                                             "url": "http://www.intuwiz.ru/articles/g02.html#.XRYVTxYza3A",
#                                                                             "win": "1090"}], "created": 1561731977216}
#
# b = {{"title": "py svg", "date": "28/8/2019", "tabs": [{"title": "PythonEffectTutorial - Inkscape Wiki",
#                                                         "url": "http://wiki.inkscape.org/wiki/index.php/PythonEffectTutorial",
#                                                         "win": "1610"}, {
#                                                            "title": "Welcome to svgutils’s documentation! — svgutils 0.1 documentation",
#                                                            "url": "https://svgutils.readthedocs.io/en/latest/",
#                                                            "win": "1610"},
#                                                        {"title": "Python Module Index — svgutils 0.1 documentation",
#                                                         "url": "https://svgutils.readthedocs.io/en/latest/py-modindex.html",
#                                                         "win": "1610"}, {
#                                                            "title": "2.1. transform – basic SVG transformations — svgutils 0.1 documentation",
#                                                            "url": "https://svgutils.readthedocs.io/en/latest/transform.html",
#                                                            "win": "1610"}, {
#                                                            "title": "2.2. compose – easy figure composing — svgutils 0.1 documentation",
#                                                            "url": "https://svgutils.readthedocs.io/en/latest/compose.html",
#                                                            "win": "1610"},
#                                                        {"title": "pySVG - Creating SVG with Python - codeboje",
#                                                         "url": "https://codeboje.de/pysvg/", "win": "1610"},
#                                                        {"title": "pysvg · PyPI",
#                                                         "url": "https://pypi.org/project/pysvg/#files", "win": "1610"},
#                                                        {"title": "alorence/pysvg-py3: Python 3 portage of pysvg",
#                                                         "url": "https://github.com/alorence/pysvg-py3", "win": "1610"},
#                                                        {
#                                                            "title": "cduck/drawSvg: A Python 3 library for programmatically generating SVG images (vector drawings) and rendering them or displaying them in an iPython notebook",
#                                                            "url": "https://github.com/cduck/drawSvg", "win": "1610"}, {
#                                                            "title": "stevelittlefish/easysvg: Simple SVG library for Python3",
#                                                            "url": "https://github.com/stevelittlefish/easysvg",
#                                                            "win": "1610"}, {
#                                                            "title": "deeplook/svglib: Read SVG files and convert them to other formats.",
#                                                            "url": "https://github.com/deeplook/svglib", "win": "1610"},
#                                                        {
#                                                            "title": "CrazyPython/svgmanip: A pythonic library for rotating, positioning, and exporting SVGs",
#                                                            "url": "https://github.com/CrazyPython/svgmanip",
#                                                            "win": "1610"}, {
#                                                            "title": "mossblaser/svgoutline: A Python library which extracts strokes (outlines) from an SVG file as a series of line segments appropriate for driving pen plotters",
#                                                            "url": "https://github.com/mossblaser/svgoutline",
#                                                            "win": "1610"},
#                                                        {"title": "nvictus/svgpath2mpl: SVG path parser for matplotlib",
#                                                         "url": "https://github.com/nvictus/svgpath2mpl", "win": "1610"},
#                                                        {
#                                                            "title": "mathandy/svgpathtools: A collection of tools for manipulating and analyzing SVG Path objects and Bezier curves.",
#                                                            "url": "https://github.com/mathandy/svgpathtools",
#                                                            "win": "1610"},
#                                                        {"title": "regebro/svg.path: SVG path objects and parser",
#                                                         "url": "https://github.com/regebro/svg.path", "win": "1610"}],
#       "created": 1567000613315}}
