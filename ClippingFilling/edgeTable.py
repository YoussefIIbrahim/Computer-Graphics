# Python version 3.6
import copy
import sys

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton

WIDTH = 500
HIGHT = 480

edges = []
edges_slave = []


def sign(x):
    if (x > 0):
        return 1
    elif (x < 0):
        return -1
    else:
        return 0


class Example(QWidget):
    def __init__(self):
        super().__init__()

        # start GUI
        self.initUI()

        # Start Scan line edge table algorithm
        self.ScanlineAlgorithm(edges, edges_slave)

    def ScanlineAlgorithm(self, x, y):
        self.x = x
        self.y = y
        self.n = len(x)

        self.xMinY = np.zeros(self.n, dtype=np.float64)
        self.minYs = np.zeros(self.n, dtype=np.uint8)
        self.maxYs = np.zeros(self.n, dtype=np.uint8)
        self.goblalEdgesr = np.zeros(self.n, dtype=np.uint8)
        self.iSlopes = np.zeros(self.n, dtype=np.float64)
        self.buildEdgeTable()

    def buildEdgeTable(self):
        i1 = None
        i2 = None
        x1 = None
        x2 = None
        y1 = None
        y2 = None
        self.edgesr = 0

        for i1 in range(self.n):
            if i1 == self.n - 1:
                i2 = 0
            else:
                i2 = i1 + 1

            y1 = self.y[i1]
            y2 = self.y[i2]
            x1 = self.x[i1]
            x2 = self.x[i2]

            if y1 == y2:
                continue

            if y1 > y2:
                tmp = y1
                y1 = y2
                y2 = tmp
                tmp = x1
                x1 = x2
                x2 = tmp

            iSlope = (x2 - x1) / (y2 - y1)
            self.minYs[self.edgesr] = y1
            self.maxYs[self.edgesr] = y2

            if y1 < y2:
                self.xMinY[self.edgesr] = x1
            else:
                self.xMinY[self.edgesr] = x2

            self.iSlopes[self.edgesr] = iSlope
            self.edgesr += 1

        self.activeEdgesr = 0

    def activateEdgesr(self, y):
        for i in range(self.edgesr):
            edge = i
            if y == self.minYs[edge]:
                index = 0
                while (index < self.activeEdgesr) and (self.xMinY[edge] > self.xMinY[self.goblalEdgesr[index]]):
                    index += 1

                for j in reversed(range(self.activeEdgesr - 1, index)):
                    self.goblalEdgesr[j + 1] = self.goblalEdgesr[j]

                self.goblalEdgesr[index] = edge
                self.activeEdgesr += 1

    def removeInactiveEdgesr(self, y):
        i = 0
        while i < self.activeEdgesr:
            index = self.goblalEdgesr[i]
            if y < self.minYs[index] or y >= self.maxYs[index]:
                for j in range(i, self.activeEdgesr - 1):
                    self.goblalEdgesr[j] = self.goblalEdgesr[j + 1]
                    self.activeEdgesr -= 1
            else:
                i += 1

    def updateXCoordinates(self):
        index = None
        x1 = -sys.float_info.max
        x2 = None
        sorted = True

        for i in range(self.activeEdgesr):
            index = self.goblalEdgesr[i]
            x2 = self.xMinY[index] + self.iSlopes[index]
            self.xMinY[index] = x2
            if x2 < x1:
                sorted = False
            x1 = x2

        if not sorted:
            self.sortActiveEdgesr()

    def sortActiveEdgesr(self):
        minim = None
        tmp = None
        for i in range(self.activeEdgesr):
            min = i
            for j in range(i, self.activeEdgesr):
                if self.xMinY[self.goblalEdgesr[j]] < self.xMinY[self.goblalEdgesr[min]]:
                    min = j

            tmp = self.goblalEdgesr[min]
            self.goblalEdgesr[min] = self.goblalEdgesr[i]
            self.goblalEdgesr[i] = tmp

    def Fill(self):

        minY = int(min(self.y))
        maxY = int(max(self.y))
        x1 = None
        x2 = None
        for y in range(minY, maxY):
            self.removeInactiveEdgesr(y)
            self.activateEdgesr(y)
            for i in range(0, self.activeEdgesr, 2):
                x1 = int(self.xMinY[self.goblalEdgesr[i]] + 0.5)
                x2 = int(self.xMinY[self.goblalEdgesr[i + 1]] + 0.5)
                for x in range(x1, x2):
                    self.image.setPixel(x, y, self.colorhelp)
            self.updateXCoordinates()

    def fillHelper(self, x_zatravka, y_zatravka):
        stack = [[x_zatravka, y_zatravka]]
        fill_color = self.colormain
        line_color = QColor(0, 0, 0)
        line_color = line_color.rgb()
        while (len(stack)):
            QApplication.processEvents()
            x, y = stack.pop()
            self.image.setPixel(x, y, fill_color)
            temp_x = x

            while (self.image.pixelColor(x, y).rgb() != line_color):
                self.image.setPixel(x, y, fill_color)
                x += 1
            x_prav = x - 1

            x = temp_x
            while (self.image.pixelColor(x, y).rgb() != line_color):
                self.image.setPixel(x, y, fill_color)
                x -= 1

            self.repaint()

            x_lev = x + 1

            x = x_lev
            y += 1
            while (x <= x_prav):
                flag = False
                while (self.image.pixelColor(x, y).rgb() != line_color and self.image.pixelColor(x,
                                                                                                 y).rgb() != fill_color and x <= x_prav):
                    if flag == False:
                        flag = True
                    x += 1

                if flag == True:
                    if (self.image.pixelColor(x, y).rgb() != line_color and self.image.pixelColor(x,
                                                                                                  y).rgb() != fill_color and x == x_prav):
                        stack.append([x, y])
                    else:
                        stack.append([x - 1, y])
                    flag = False

                x_vhod = x
                while (self.image.pixelColor(x, y).rgb() != line_color and self.image.pixelColor(x,
                                                                                                 y).rgb() != fill_color and x < x_prav):
                    x += 1

                if x == x_vhod:
                    x += 1
            x = x_lev
            y -= 2
            # Second part
            while (x <= x_prav):
                flag = False
                while (self.image.pixelColor(x, y).rgb() != line_color and self.image.pixelColor(x,
                                                                                                 y).rgb() != fill_color and x <= x_prav):
                    if flag == False:
                        flag = True
                    x += 1

                if flag == True:
                    if (self.image.pixelColor(x, y).rgb() != line_color and self.image.pixelColor(x,
                                                                                                  y).rgb() != fill_color and x == x_prav):
                        stack.append([x, y])
                    else:
                        stack.append([x - 1, y])
                    flag = False

                x_vhod = x
                while (self.image.pixelColor(x, y).rgb() != line_color and self.image.pixelColor(x,
                                                                                                 y).rgb() != fill_color and x < x_prav):
                    x += 1

                if x == x_vhod:
                    x += 1

    def Bresenham(self, x1, y1, x2, y2, color=QColor(0, 0, 0).rgb()):
        dx = int(x2 - x1)
        dy = int(y2 - y1)
        sx = sign(dx)
        sy = sign(dy)
        dx = abs(dx)
        dy = abs(dy)

        swap = False
        if (dy <= dx):
            swap = False
        else:
            swap = True
            dx, dy = dy, dx

        e = int(2 * dy - dx)
        x = int(x1)
        y = int(y1)

        for i in range(dx + 1):
            self.image.setPixel(x, y, color)
            if (e >= 0):
                if (swap):
                    x += sx
                else:
                    y += sy
                e = e - 2 * dx
            if (e < 0):
                if (swap):
                    y += sy
                else:
                    x += sx
                e = e + 2 * dy

    def CMidpoint(self):
        fill_color = QColor(0, 0, 0).rgb()
        xc = int(self.zpx.text())
        yc = int(self.zpy.text())
        R = 50

        p = int(1 - R)
        x = 0
        y = R

        self.image.setPixel(int(xc + x), int(yc + y), fill_color)
        self.image.setPixel(int(xc + x), int(yc - y), fill_color)
        self.image.setPixel(int(xc - x), int(yc + y), fill_color)
        self.image.setPixel(int(xc - x), int(yc - y), fill_color)
        self.image.setPixel(int(xc + y), int(yc + x), fill_color)
        self.image.setPixel(int(xc + y), int(yc - x), fill_color)
        self.image.setPixel(int(xc - y), int(yc + x), fill_color)
        self.image.setPixel(int(xc - y), int(yc - x), fill_color)

        while (x < y):
            x += 1
            if (p < 0):
                p += 2 * x + 1
            else:
                y -= 1
                p += 2 * (x - y) + 1

            self.image.setPixel(int(xc + x), int(yc + y), fill_color)
            self.image.setPixel(int(xc + x), int(yc - y), fill_color)
            self.image.setPixel(int(xc - x), int(yc + y), fill_color)
            self.image.setPixel(int(xc - x), int(yc - y), fill_color)
            self.image.setPixel(int(xc + y), int(yc + x), fill_color)
            self.image.setPixel(int(xc + y), int(yc - x), fill_color)
            self.image.setPixel(int(xc - y), int(yc + x), fill_color)
            self.image.setPixel(int(xc - y), int(yc - x), fill_color)

    def initUI(self):
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle('Points')
        self.Group = QHBoxLayout(self)
        self.v = QVBoxLayout()
        self.GraphView = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.image = QImage(WIDTH, HIGHT - 20, QImage.Format_RGB32)

        self.Group.addWidget(self.GraphView)
        self.Group.addLayout(self.v)
        self.image.fill(Qt.white)

        self.GraphView.setGeometry(10, 10, WIDTH, HIGHT)
        self.GraphView.setStyleSheet("background-color: white")
        self.scene.addPixmap(QPixmap.fromImage(self.image))

        self.GraphView.setScene(self.scene)

        self.fill_butt = QPushButton('Fill', self)
        self.fill_butt.resize(self.fill_butt.sizeHint())

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["x", "y"])
        self.v.addWidget(self.table)

        v1 = QHBoxLayout()

        self.clear = QPushButton('Clear', self)
        self.clear.resize(self.fill_butt.sizeHint())
        v1.addWidget(self.clear)

        self.Add = QPushButton('Add', self)
        self.Add.resize(self.fill_butt.sizeHint())
        v1.addWidget(self.Add)
        self.v.addLayout(v1)
        self.v.addWidget(self.fill_butt)

        v2 = QVBoxLayout()
        v3 = QHBoxLayout()
        v4 = QHBoxLayout()
        self.v.addLayout(v2)
        self.zplbl = QLabel(self)
        self.zplbl.setText("The seed pixel:")

        self.zpx = QLineEdit(self)
        self.zpx.setText("0")

        self.zpxlbl = QLabel(self)
        self.zpxlbl.setText("X = ")
        v3.addWidget(self.zpxlbl)
        v3.addWidget(self.zpx)

        self.zpy = QLineEdit(self)
        self.zpy.setText("0")

        self.zpylbl = QLabel(self)
        self.zpylbl.setText("Y = ")
        v4.addWidget(self.zpylbl)
        v4.addWidget(self.zpy)

        self.rb3 = QRadioButton(self)
        self.rb3.setText("Center Point")

        self.rb2 = QRadioButton(self)
        self.rb2.setText("Polygon")
        self.rb2.setChecked(True)

        self.color_button = QPushButton(self)
        self.color_button.setGeometry(800, 100, 40, 20)

        v2.addWidget(self.color_button)
        v2.addWidget(self.rb2)
        v2.addWidget(self.rb3)
        v2.addWidget(self.zplbl)
        v2.addLayout(v3)
        v2.addLayout(v4)

        self.colormain = QColor(0, 255, 0).rgb()
        self.color_button.setStyleSheet('QPushButton{background-color:' + QColor(0, 255, 0).name() + '}')
        self.capslock = False

        self.color_button.clicked.connect(lambda: self.GetColor())
        self.Add.clicked.connect(lambda: self.ShowDialog())
        self.fill_butt.clicked.connect(lambda: self.EdgeFill())
        self.clear.clicked.connect(lambda: self.Clear())
        self.show()

    def keyPressEvent(self, QKeyEvent):
        if (QKeyEvent.key() == 67 or QKeyEvent.key() == 99):
            self.CMidpoint()
        elif QKeyEvent.key() == 16777252:
            self.capslock = not self.capslock

    def GetColor(self):
        color = QColorDialog.getColor()
        self.colormain = color.rgb()
        hexcolor = color.name()
        self.color_button.setStyleSheet('QPushButton{background-color:' + hexcolor + '}')

    def EdgeFill(self):
        self.draw_borders()
        x_zatr = int(self.zpx.text())
        y_zatr = int(self.zpy.text())
        self.fillHelper(x_zatr, y_zatr)

    def ShowDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter X Y:')
        if ok:
            text = text.split()
            x = int(text[0])
            y = int(text[1])
            i = len(edges_slave)
            if i:
                self.Bresenham(edges_slave[i - 1][0], edges_slave[i - 1][1], x, y)
            edges_slave.append([x, y])
            self.table_appender([x, y])

    def Clear(self):
        edges.clear()
        edges_slave.clear()
        self.table.setRowCount(0)
        self.image.fill(Qt.white)

    def draw_borders(self):
        for j in range(len(edges)):
            for i in range(len(edges[j]) - 1):
                self.Bresenham(edges[j][i][0], edges[j][i][1], edges[j][i + 1][0], edges[j][i + 1][1])
        self.repaint()

    def mousePressEvent(self, QMouseEvent):
        if (QMouseEvent.button() == Qt.LeftButton):
            cord = QMouseEvent.pos()
            if self.rb3.isChecked():
                y = cord.y()
                x = cord.x()
                self.zpx.setText(str(x - 10))
                self.zpy.setText(str(y - 10))
                return

            y = cord.y()
            x = cord.x()
            if (x >= 10 and y >= 10 and y <= HIGHT and x <= WIDTH):
                x -= 10
                y -= 10
                i = len(edges_slave)

                if self.capslock and i:
                    if y != edges_slave[i - 1][1]:
                        der = (x - edges_slave[i - 1][0]) / (y - edges_slave[i - 1][1])
                    else:
                        der = 2
                    if abs(der) <= 1:
                        x = edges_slave[i - 1][0]
                    else:
                        y = edges_slave[i - 1][1]

                if i:
                    self.Bresenham(edges_slave[i - 1][0], edges_slave[i - 1][1], x, y)
                edges_slave.append([x, y])
                self.table_appender([x, y])


        elif (QMouseEvent.button() == Qt.RightButton):
            i = len(edges_slave)
            if i:
                x = edges_slave[0][0]
                y = edges_slave[0][1]
                self.Bresenham(edges_slave[i - 1][0], edges_slave[i - 1][1], x, y)
                edges_slave.append([x, y])
            edges.append(copy.deepcopy(edges_slave))
            edges_slave.clear()
            self.table_appender(['end', 'end'])

        elif QMouseEvent.button() == Qt.MiddleButton:
            cord = QMouseEvent.pos()
            y = cord.y()
            x = cord.x()
            self.zpx.setText(str(x - 10))
            self.zpy.setText(str(y - 10))

    def table_appender(self, coord):
        N = self.table.rowCount()
        self.table.setRowCount(N + 1)
        self.table.setItem(N, 0, QTableWidgetItem(str(coord[0])))
        self.table.setItem(N, 1, QTableWidgetItem(str(coord[1])))

    def paintEvent(self, e):
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Example()
    MainWindow.show()
    sys.exit(app.exec_())
