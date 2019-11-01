from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import QBrush, QColor

from cncoilgcode import CNFile

COLOR_DISABLED = '#DDDDDD'
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


class GcodeModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentFile = ".\\gcode\\vcomtest.cnc"

        self.currentDir = '\\'.join(self.currentFile.split('\\')[:-1])

        self._cnFile = CNFile(filename=self.currentFile)

        self._headers = ['#', 'Command', 'X mm', 'Y mm', 'R mm', 'Arc', 'Speed', 'Spill', 'Delay', 'Pm']
        self._data = list()

        self._init()

    def _init(self):
        self.beginResetModel()
        self._data = self._cnFile._commands
        self.endResetModel()

    def loadDesign(self, filename):
        self._cnFile = CNFile(filename=filename)
        self._init()

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

        if not self.flags(index) & Qt.ItemIsEnabled and col != 0:
            if role == Qt.BackgroundRole:
                return QVariant(QBrush(QColor(COLOR_DISABLED)))
            return QVariant()

        if role == Qt.DisplayRole:
            if not self._data:
                return QVariant()
            return QVariant(str(self._data[row][col]))

        return QVariant()

    def flags(self, index):
        f = super().flags(index)
        row = index.row()
        col = index.column()

        if col == 0:
            return f ^ Qt.ItemIsEnabled

        command = self._data[row]['gcode']
        if command == 'G01':
            if col in (5, 8, 9):
                return f ^ Qt.ItemIsEnabled

        elif command == 'G02' or command == 'G03':
            if col in (8, 9):
                return f ^ Qt.ItemIsEnabled

        elif command == 'M501':
            if col in (2, 3, 4, 5, 6, 9):
                return f ^ Qt.ItemIsEnabled

        elif command in GCODE_COMMAND_LABELS:
            if col in range(2, 9):
                return f ^ Qt.ItemIsEnabled

        return f

    @property
    def length(self):
        lng = 0
        for c in self._commands:
            lng += len(c)
        return lng
