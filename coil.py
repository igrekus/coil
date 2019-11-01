import sys
import pygcode

from PyQt5.QtWidgets import QApplication
from pygcode import Line, GCodeLinearMove, GCodeArcMoveCW, GCodeArcMoveCCW, GCodeMotion

from mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

# d = {"title": "qt arc", "date": "14/6/2019", "tabs": [{"title": "qgraphicsitem arc - Поиск в Google",
#                                                        "url": "https://www.google.com/search?q=qgraphicsitem+arc&oq=qgraphicsitem+arc&aqs=chrome..69i57.4945j0j7&sourceid=chrome&ie=UTF-8",
#                                                        "win": "1090"},
#                                                       {"title": "c++ - QT QGraphicsScene Drawing Arc - Stack Overflow",
#                                                        "url": "https://stackoverflow.com/questions/14279162/qt-qgraphicsscene-drawing-arc",
#                                                        "win": "1090"},
#                                                       {"title": "c++ - Arc in QGraphicsScene - Stack Overflow",
#                                                        "url": "https://stackoverflow.com/questions/26901540/arc-in-qgraphicsscene",
#                                                        "win": "1090"},
#                                                       {
#                                                           "title": "(SOLVED) Draw arc into qgraphicsview | Qt Forum",
#                                                           "url": "https://forum.qt.io/topic/47365/solved-draw-arc-into-qgraphicsview/6",
#                                                           "win": "1090"},
#                                                       {
#                                                           "title": "QGraphicsView / QPainter / QGraphicsItem arc drawing bug.",
#                                                           "url": "https://www.qtcentre.org/threads/64852-QGraphicsView-QPainter-QGraphicsItem-arc-drawing-bug",
#                                                           "win": "1090"},
#                                                       {
#                                                           "title": "Qt5 Tutorial Qt5 Customizing Items by inheriting QGraphicsItem - 2016",
#                                                           "url": "https://www.bogotobogo.com/Qt/Qt5_QGraphicsView_QGraphicsScene_QGraphicsItems.php",
#                                                           "win": "1090"}], "created": 1560515518174}
