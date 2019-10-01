import os

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from pygcode import Line


class Command:
    def __init__(self, text):
        self._text: str = text.strip()

        self._command = ''
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

        self._parse()

    def _parse(self):
        if self._text == 'G71':
            self._gcode = 'G71'
            self._command = 'Старт'
        elif self._text == 'G90':
            self._gcode = 'G90'
            self._command = 'Абс'
        elif self._text == 'M30':
            self._gcode = 'M30'
            self._command = 'Конец'
        elif self._text.startswith('N'):
            ts = self._text.split('\n')
            print(ts)
            if len(ts) == 1:
                params = ts[0].split(' ')
                self._index = int(params[0][1:4])
                self._gcode = params[1]
                self._pm = int(params[2][1:])

                gcode = params[1]
                if gcode == 'M70':
                    self._command = 'Weld'
                elif gcode == 'M71':
                    self._command = 'Sono up'
                elif gcode == 'M72':
                    self._command = 'Sono mid'
                elif gcode == 'M73':
                    self._command = 'Sono low'
                elif gcode == 'M74':
                    self._command = 'Cut wire'
                elif gcode == 'M75':
                    self._command = 'Embed on'
                elif gcode == 'M76':
                    self._command = 'Embed off'
                elif gcode == 'M77':
                    self._command = 'Pull wire'
                elif gcode == 'M78':
                    self._command = 'Hold module'
                elif gcode == 'M79':
                    self._command = 'Release module'
                elif gcode == 'M80':
                    self._command = 'Brake on'
                elif gcode == 'M81':
                    self._command = 'Brake off'
                elif gcode == 'M82':
                    self._command = 'Thermode mid'
                elif gcode == 'M83':
                    self._command = 'Thermode up'

            else:
                pass

    def __str__(self):
        return f'Command(text={self._text})'

    def __getitem__(self, item):
        if item == 0:
            return self._index
        elif item == 1:
            return self._command
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


class GcodeModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._gcode_file = "C:\\devtools\\CNCoil\\CNCFILES\\vtest.cnc"
        # self._gcode_file = "C:\\devtools\\CNCoil\\CNCFILES\\vexp10n_.cnc"

        self._headers = list()
        self._data = list()

        self._commands = list()

        self._init()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data.clear()
        self.endRemoveRows()

    def _init(self):
        if os.path.isfile(self._gcode_file):
            with open(self._gcode_file, mode='rt') as f:
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

        return QVariant()

    # def flags(self, index):
    #     f = super(BillTableModel, self).flags(index)
    #     if index.column() == self.ColumnActive or index.column() == self.ColumnStatus:
    #         f = f | Qt.ItemIsUserCheckable
    #     return f
