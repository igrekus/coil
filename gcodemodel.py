import math
import os

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import QBrush, QColor
from pygcode import Line


COLOR_DISABLED = '#F5F5F5'
GCODE_COMMAND_LABELS = {
    'M70': 'Weld',
    'M71': 'Sono up',
    'M72': 'Sono mid',
    'M73': 'Sono low',
    'M74': 'Cut wire',
    'M75': 'Embed on',
    'M76': 'Embed off',
    'M77': 'Pull wire',
    'M78': 'Hold module',
    'M79': 'Release module',
    'M80': 'Brake on',
    'M81': 'Brake off',
    'M82': 'Thermode mid',
    'M83': 'Thermode up'
}


class Command:
    def __init__(self, text):
        self._text: str = text.strip()

        self._label = ''
        self._index = ''
        self._x = ''
        self._y = ''
        self._r = ''
        self._arc = ''
        self._speed = ''
        self._spill = ''
        self._delay = ''
        self._pm = ''

        self._gcode = ''
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

                self._x = float(params[0][1:])
                self._y = float(params[1][1:])
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
                    self._r = round(math.sqrt(pow(self._x - i, 2) + pow(self._y - j, 2)))

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

                    self._x = float(params2[0][1:])
                    self._y = float(params2[1][1:])

                    i1, j1 = float(params1[3][1:]), float(params1[4][1:])
                    r1 = round(math.sqrt(pow(float(params1[0][1:]) - i1, 2) + pow(float(params1[1][1:]) - j1, 2)))
                    self._r = r1

                    # i2, j2 = float(params2[3][1:]), float(params2[4][1:])
                    # r2 = round(math.sqrt(pow(self._x - i2, 2) + pow(self._y - j2, 2)))

                else:
                    # line + arc
                    pass


    def __str__(self):
        return f'Command(text={self._text})'

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


class GcodeModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # self.currentFile = "C:\\devtools\\CNCoil\\CNCFILES\\vtest.cnc"
        self.currentFile = 'C:\\devtools\\CNCoil\\CNCFILES\\vtest1.cnc'
        # self.currentFile = "C:\\devtools\\CNCoil\\CNCFILES\\vgeotest.cnc"
        # self.currentFile = "C:\\devtools\\CNCoil\\CNCFILES\\vexp10n_.cnc"
        self.currentDir = 'C:\\devtools\\CNCoil\\CNCFILES'

        self._headers = list()
        self._data = list()

        self._commands = list()

        self._init()

    def _init(self):
        self.loadDesign(self.currentFile)

    def loadDesign(self, filename):
        self._commands.clear()

        if os.path.isfile(filename):
            with open(filename, mode='rt') as f:
                command_block = ''
                for l in f.readlines():
                    l = l.strip()
                    if r'//' in l or r'%' in l or ':' in l or not l:
                        continue

                    elif l.startswith('N'):
                        if not command_block:
                            command_block = l
                            continue
                        else:
                            self._commands.append(Command(command_block))
                            command_block = l
                    elif 'G71' in l or 'G90' in l or 'M30' in l:
                        if command_block:
                            self._commands.append(Command(command_block))
                            command_block = ''
                        self._commands.append(Command(l))
                        continue
                    else:
                        command_block += '\n' + l

        self._updateModel()

    def _updateModel(self):
        self.beginResetModel()
        self._headers = ['#', 'Command', 'X mm', 'Y mm', 'R mm', 'Arc', 'Speed', 'Spill', 'Delay', 'Pm']
        self._data = self._commands
        self.endResetModel()

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self._headers):
                    return QVariant(self._headers[section])
            if orientation == Qt.Vertical:
                if section < len(self._data):
                    return QVariant(section + 1)

        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        # FIXME: row counter
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._headers)

    # def setData(self, index, value, role):
    #     if role == Qt.CheckStateRole:
    #         item = self._modelDomain.getBillItemAtIndex(index)
    #         if index.column() == self.ColumnActive:
    #             tmplist = self._modelDomain._rawPlanData[item.item_id].copy()
    #             if value == 0:
    #                 tmplist[2] = 0
    #             elif value > 0:
    #                 tmplist[2] = 1
    #             self._modelDomain._rawPlanData[item.item_id] = tmplist
    #             return True
    #
    #         if index.column() == self.ColumnStatus:
    #             if value == 0:
    #                 item.item_status = 2
    #                 item.item_priority = 3
    #             elif value == 2:
    #                 item.item_status = 1
    #                 item.item_priority = 1
    #
    #             self._modelDomain.updateBillItem(index, item)
    #
    #             self.dataChanged.emit(self.index(index.row(), self.ColumnId, QModelIndex()),
    #                                   self.index(index.row(), self.ColumnActive, QModelIndex()), [])
    #             return True
    #
    #     return False

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if not self._data:
                return QVariant()
            return QVariant(str(self._data[row][col]))

        if role == Qt.BackgroundRole:
            row = index.row()
            col = index.column()

            if row == 0 or row == 1 or row == len(self._data) - 1:
                return QVariant(QBrush(QColor(COLOR_DISABLED)))

            command = self._data[row]['gcode']
            if command == 'G01':
                if col in (5, 8, 9):
                    return QVariant(QBrush(QColor(COLOR_DISABLED)))

            if command == 'G02' or command == 'G03':
                if col in (8, 9):
                    return QVariant(QBrush(QColor(COLOR_DISABLED)))

            if command in GCODE_COMMAND_LABELS:
                if col in range(2, 9):
                    return QVariant(QBrush(QColor(COLOR_DISABLED)))

        return QVariant()

    def flags(self, index):
        f = super().flags(index)
        row = index.row()
        col = index.column()

        if col == 0:
            return f ^ Qt.ItemIsEnabled

        if row == 0 or row == 1 or row == len(self._data) - 1:
            return f ^ Qt.ItemIsEnabled

        command = self._data[row]['gcode']
        if command == 'G01':
            if col in (5, 8, 9):
                return f ^ Qt.ItemIsEnabled

        elif command == 'G02' or command == 'G03':
            if col in (8, 9):
                return f ^ Qt.ItemIsEnabled

        elif command in GCODE_COMMAND_LABELS:
            if col in range(2, 9):
                return f ^ Qt.ItemIsEnabled

        return f
