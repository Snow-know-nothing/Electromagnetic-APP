import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from plot_pyqt import PlotCanvas


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 matplotlib example')
        self.setGeometry(10,10,600,400)

        m = PlotCanvas(self)
        m.move(0,0)
        
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())