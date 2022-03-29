from __future__ import division #整数除法 / 变为普通除法
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import numpy as np
from sympy import *
import time
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import (QEvent, QTimer, Qt)
from PyQt5.QtGui import QPainter
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
x_data = 0;y_data = 0;

'''
注意：
1.仅可以求解常微分方程
2.输入的时候使用英文输入法，当使用中文输入法的时候会出现不可预知的错误
3.这个demo中，text仅仅只能作为接收信息的工具，不要用来处理信息
eg.:
10*(y-x),x*(28-z),x*y-3*z
0,30,0.01
0,1,0
'''

x, y, z, t = symbols('x, y, z, t', real=True)
f = Function('f')
func_x_tmp = '10*(y-x)'
func_y_tmp = 'x*(28-z)'
func_z_tmp = 'x*y-3*z'
T_tmp = '0,30,0.01'
bound_tmp = '0,1,0'

class T:
    start = 0
    stop = 30
    step = 3000
    length = 0.01

    def data(self):
        return np.arange(self.start, self.stop, self.length)

T = T()

boundary = (0, 1., 0)



class Myfigure(FigureCanvas):
    def __init__(self):
        self.fig = plt.figure(figsize=(4,4))  # 可选参数,facecolor为背景颜色facecolor='#FFD7C4',
        # self.axes = self.fig.subplots() #也可以用add_subplot
        self.axes = Axes3D(self.fig)
        FigureCanvas.__init__(self, self.fig) #初始化激活widget中的plt部分
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.axes.mouse_init()
        
    def _print(self):
        
        self.draw()

    def on_press(self,event):
        global x_data, y_data
        x_data = event.xdata
        y_data = event.ydata
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)

class Main_window(QWidget):
    def __init__(self):
        super(Main_window, self).__init__()

        # QWidget
        self.figure = Myfigure()
        self.setWindowTitle('Axes3d display')
        # self.fig_ntb = NavigationToolbar(self.figure, self) #注意，记得指向figure的FigureCanvas
        self.button_text = QPushButton("确认输入")
        self.button_text.setFont(QFont( "Roman times" , 10 ,  QFont.Bold))

        self.text1 = QLineEdit('')
        self.text1.setPlaceholderText('输入需要求解的表达式1')
        self.text1.textChanged.connect(self.text_handler1)
        self.text2 = QLineEdit('')
        self.text2.setPlaceholderText('输入需要求解的表达式2')
        self.text2.textChanged.connect(self.text_handler2)
        self.text3 = QLineEdit('')
        self.text3.setPlaceholderText('输入需要求解的表达式3')
        self.text3.textChanged.connect(self.text_handler3)
        self.text4 = QLineEdit('')
        self.text4.setPlaceholderText('输入需要求解的时域:start,stop,step')
        self.text4.textChanged.connect(self.text_handler4)
        self.text5 = QLineEdit('')
        self.text5.setPlaceholderText('输入需要求解的边界:x[0],y[0],z[0]')
        self.text5.textChanged.connect(self.text_handler5)


        self.label = QLabel('')
        self.label.setFont(QFont( "Roman times" , 8 ,  QFont.Bold))

        timer = QTimer(self)  #设置一个定时器用来刷新label显示的坐标
        timer.timeout.connect(self.time_Event)
        timer.start(1000)
        # 连接事件
        # self.button_draw.clicked.connect(self.figure.Draw)
        self.button_text.clicked.connect(self.but_click)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.text1)
        layout.addWidget(self.text2)
        layout.addWidget(self.text3)
        layout.addWidget(self.text4)
        layout.addWidget(self.text5)
        layout.addWidget(self.figure)
        # layout.addWidget(self.fig_ntb)
        layout.addWidget(self.button_text)
        layout.addWidget(self.label)
        self.setLayout(layout)


    def time_Event(self):
        data_xy = str(x_data)+','+str(y_data)
        self.label.setText(data_xy)

    def text_handler1(self,text):
        global func_x_tmp
        func_x_tmp = text

    def text_handler2(self,text):
        global func_y_tmp
        func_y_tmp = text

    def text_handler3(self,text):
        global func_z_tmp
        func_z_tmp = text

    def text_handler4(self,text):
        global T_tmp
        T_tmp = text

    def text_handler5(self,text):
        global bound_tmp
        bound_tmp = text

    def but_click(self):
        output = self.data_handler()
        self.figure.axes.plot(output[:,0],output[:,1],output[:,2])
        self.figure._print()
        self.button_text.setText('关闭窗口')
        self.button_text.clicked.disconnect(self.but_click)
        self.button_text.clicked.connect(self.close)

    def data_handler(self):
        global x, y, z, boundary, T_tmp, bound_tmp, T
        global data_x, data_y, data_z
        T_tmp = [float(i) for i in T_tmp.split(',')]

        boundary = tuple(float(i) for i in bound_tmp.split(','))

        T.start = T_tmp[0];T.stop = T_tmp[1];T.length = T_tmp[2]

        def func(w,t):
            global func_x_tmp, func_y_tmp, func_z_tmp, x, y, z
            x, y, z = w
            X = eval(func_x_tmp)
            Y = eval(func_y_tmp)
            Z = eval(func_z_tmp)

            return np.array([X, Y, Z])

        output = odeint(func, boundary, T.data())

        # data_x[0], data_y[0], data_z[0] = boundary #这边用于拓展输出x,y,z
        # data_x[1,:] = output[:,0]
        # data_y[1,:] = output[:,1]
        # data_z[1,:] = output[:,2]

        return output




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main_window()
    ui.show()
    sys.exit(app.exec_())

