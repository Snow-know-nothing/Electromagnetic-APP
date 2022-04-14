from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None,width=8,height=7,mode=2):
        fig = plt.figure(figsize=(width, height), dpi=100)
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.mode = mode
        if mode == 1:
            self.ax1 = self.figure.add_subplot(1,1,1)
        elif mode == 2:
            self.ax1 = self.figure.add_subplot(2,1,1)
            self.ax2 = self.figure.add_subplot(2,1,2)
            

    def plottest(self):
        n = np.random.rand(100)
        data = np.sin(10*n)
        ax = self.figure.add_subplot(2,1,1)
        ax.set_title('PyQt Matplotlib Example')
        ax.plot(data, 'r-')
        ax2 = self.figure.add_subplot(2,1,2)
        ax2.plot(n, 'b-.')
        self.show()

    def plot(self,z,E1,H1,xlim):
        if self.mode == 2:
            #print("here")
            # 电场画图
            self.ax1.cla()
            self.ax1.plot(z,E1, color='blue', alpha=0.5)
            self.ax1.fill_between(z, 0, E1, color='blue', alpha=.25)  # 填充两个函数之间的区域，本例中填充（0和Y+1之间的区域）
            #self.ax1.set_xlim(0,xlim)
            self.ax1.set_ylim(-6, 6)
            #ax.xlabel('Spatial location')
            #ax.ylabel('Electric field strength')
            self.ax1.set_title('Electric Wave')

            # 磁场画图
            self.ax2.cla()
            self.ax2.plot(z,H1, color='red', alpha=0.5)
            self.ax2.fill_between(z, 0, H1, color='red', alpha=.25)  # 填充两个函数之间的区域，本例中填充（0和Y+1之间的区域）
            #self.ax2.set_xlim(0,xlim)
            self.ax2.set_ylim(-6, 6)                         # 统一坐标轴，便于合并前后的流畅
            #self.ax2.set_xlabel('Spatial location')
            #ax2.ylabel('Magnetic induction')
            self.ax2.set_title('Magnetic Wave')
        elif self.mode == 1:
            self.ax1.cla()
             # 电场
            self.ax1.plot(z, E1, color='blue', alpha=0.5)
            self.ax1.fill_between(z, 0, E1, color='blue', alpha=.25)  # 填充两个函数之间的区域，本例中填充（0和Y+1之间的区域）

            # 磁场
            self.ax1.plot(z, H1, color='red', alpha=0.5)
            self.ax1.fill_between(z, 0, H1, color='red', alpha=.25)  # 填充两个函数之间的区域，本例中填充（0和Y+1之间的区域）
            #plt.xlim(0,n * lambda1)
            self.ax1.set_ylim(-10, 10)
            #plt.xlabel('Spatial location')
            #plt.ylabel('Electric and Magnetic field strength')
            self.ax1.set_title('Electric && Magnetic  Wave')

        self.draw()

class PlotCanvas3D(FigureCanvas):

    def __init__(self, parent=None):
        self.fig = plt.figure(figsize=(5,5))  # 可选参数,facecolor为背景颜色facecolor='#FFD7C4',
        # self.axes = self.fig.subplots() #也可以用add_subplot
        self.axes = Axes3D(self.fig)
        FigureCanvas.__init__(self, self.fig) #初始化激活widget中的plt部分
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.axes.mouse_init()

    def plot3D(self,x,y,z,E1,H1,xlim):
        self.axes.cla()
        # x,y = np.meshgrid(10,10)
        self.axes.quiver3D(x,y,z,E1, np.zeros_like(E1), np.zeros_like(E1),color="blue")
        self.axes.quiver3D(x,y,z,np.zeros_like(H1), H1, np.zeros_like(H1),color="red")
        # self.axes.plot(E1, np.zeros_like(E1), z, c='b')
        # self.axes.plot(np.zeros_like(H1), H1, z, c='r')
        self.axes.set_xlabel('Electric field x')
        self.axes.set_ylabel('Magnetic field y')
        # fig = plt.figure()
         # ax = fig.gca(projection='3d')
         # figure1 = ax.plot3D(E1, np.zeros_like(E1), z, c='b')
         # figure2 = ax.plot3D(np.zeros_like(H1), H1, z, c='r')
        # self.axes.set_xlim(-5, 5)
        # self.axes.set_ylim(-5, 5)
        self.axes.set_title('Vertical incidence of plane wave')
        self.draw()