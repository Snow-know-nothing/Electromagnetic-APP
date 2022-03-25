from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None,width=6,height=4):
        fig = Figure(figsize=(width, height), dpi=100)
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.plot()


    def plot(self):
        n = np.random.rand(100)
        data = np.sin(10*n)
        ax = self.figure.add_subplot(2,1,1)
        ax.set_title('PyQt Matplotlib Example')
        ax.plot(data, 'r-')
        ax2 = self.figure.add_subplot(2,1,2)
        ax2.plot(n, 'b-.')
        self.show()