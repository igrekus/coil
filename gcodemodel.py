from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsLineItem

from cncoilgcode import *

COLOR_DISABLED = '#DDDDDD'


class GcodeModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentFile = ".\\gcode\\vgeotest.cnc"

        self.currentDir = '\\'.join(self.currentFile.split('\\')[:-1])

        self._cnFile = CNFile(filename=self.currentFile)

        self._headers = ['#', 'Command', 'X mm', 'Y mm', 'R mm', 'Arc', 'Speed', 'Spill', 'Delay', 'Prm']
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

        if col not in self._data[row].enabled:
            return f ^ Qt.ItemIsEnabled

        return f

    def shiftGeometry(self, direction, value, rows):
        print(direction, value, rows)

    @property
    def length(self):
        return self._cnFile.length

    @property
    def viewItems(self):
        items = list()
        zoom = 10
        for c in self._cnFile._commands:
            items.append(QGraphicsLineItem(c.p1.x * zoom, -c.p1.y * zoom, c.p2.x * zoom, -c.p2.y * zoom))
        return items
