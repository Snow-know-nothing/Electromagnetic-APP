# -*- coding: utf-8 -*-
#from pickle import TRUE
#from tkinter import image_names
from pickle import FALSE
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from field import Ui_MainWindow as UIM
from infordia import Ui_InforDialog as DIA
from plot_pyqt import PlotCanvas, PlotCanvas3D

import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

class mywindow(QtWidgets.QMainWindow,UIM):
   def __init__(self):
      super(mywindow, self).__init__()
      self.setupUi(self)
   
      image = QtGui.QPixmap()
      image.load("./image/bkg.jpg")
      image = image.scaled(self.width(), self.height())
      palette1 = QtGui.QPalette()
      palette1.setBrush(self.backgroundRole(), QtGui.QBrush(image)) #背景图片
      #palette1.setColor(w.backgroundRole(), QColor(192,253,123)) #背景颜色
      self.setPalette(palette1)
      self.setAutoFillBackground(True)

      self.actionPause.setEnabled(True)
      self.actionStart.setEnabled(False)
      #槽函数
      self.pushButton.clicked.connect(self.openimage)
      self.ch1Button.clicked.connect(self.change)
      self.actionInformation.triggered.connect(self.infodis)
      self.actionPause.triggered.connect(self.pauseit)
      self.actionStart.triggered.connect(self.startit)
      self.actionOpen_file_N.triggered.connect(self.saveit)
      #绘图例化
      self.m = PlotCanvas(self.label_2D_H_2)
      self.m.move(0,0)  

      self.n = PlotCanvas(self.label_2D_E_3,mode=1)
      self.n.move(0,0) 
      self.label_2D_E_3.hide()
      #绘图3D例化
      self.n3D = PlotCanvas3D(self.label_3D_EH)
      self.n3D.move(0,0) 
      #标志位
      self.runorpause = 1

      self.cwd = os.getcwd() # 获取当前程序文件位置
   def saveit(self):
      fileNamebase, filetype = QtWidgets.QFileDialog.getSaveFileName(self,  
                                    "文件保存",  
                                    self.cwd, # 起始路径 
                                    "All Files (*);;Text Files (*.)")  

      if fileNamebase == "":
            print("\n取消选择")
            return
      filename = fileNamebase + '1' + '.png'
      #img = self.label_2D_H_2.pixmap().toImage()
      self.m.figure.savefig(filename)
      filename = fileNamebase + '2' + '.png'
      self.n.figure.savefig(filename)
      filename = fileNamebase + '3' + '.png'
      self.n3D.figure.savefig(filename)

   def startit(self):
      self.runorpause = 1
      self.actionStart.setEnabled(False)
      self.actionPause.setEnabled(True)

   def pauseit(self):
      self.runorpause = 0
      self.actionStart.setEnabled(True)
      self.actionPause.setEnabled(False)

   def infodis(self):
      MainDialog = QtWidgets.QDialog()      # 创建一个主窗体（必须要有一个主窗体）
      myDialog = DIA()   # 创建对话框
      myDialog.setupUi(MainDialog)   # 将对话框依附于主窗体
      # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
      #MainDialog.set(Qt.ApplicationModal)
      MainDialog.show()
      MainDialog.exec_()

   def change(self):
      if (self.ch1Button.isChecked() == False):
         self.textEdit_3.setDisabled(True)
         self.textEdit_4.setDisabled(True)
         self.textEdit_5.setDisabled(True)
      else:
         self.textEdit_3.setEnabled(True)
         self.textEdit_4.setEnabled(True)
         self.textEdit_5.setEnabled(True)

   def openimage(self):
      self.runorpause = 1
      # 参数设置
      if (self.ch1Button.isChecked() == False):
         # 计算参数
         u0 = 4 * math.pi * pow(10, -7)  # 真空中介电常数
         e0 = 1 / (36 * math.pi) * pow(10, -9)  # 真空中磁导率
         # 空气的介电常数和磁导率
         u1 = u0
         e1 = e0
         omiga = float(self.textEdit_2.text()) *2* math.pi # 频率
         k1 = omiga * math.sqrt(u1 * e1)  # 波数k1
         eta1 = math.sqrt(u1 / e1)  # 复波阻抗
         Ei0 = float(self.textEdit.text())  # 初始场强
         lambda1 = 2 * math.pi / k1  # 波长
         fai = 0
         alpha = 0
         n = 6  # 波形起始位置
         z = np.linspace(0,n * lambda1, 100)
      else:
      # 计算参数
         u0 = 4 * math.pi * pow(10, -7)  # 真空中介电常数
         e0 = 1 / (36 * math.pi) * pow(10, -9)  # 真空中磁导率
         # 空气的介电常数和磁导率
         u1 = u0
         e1 = e0
         omiga = float(self.textEdit_2.text()) *2* math.pi  # 频率
         k1 = 2 * math.pi # 波数k1
         eta1 = float(self.textEdit_5.text()) * math.pi # 复波阻抗
         Ei0 = float(self.textEdit.text())  # 初始场强
         lambda1 = 2 * math.pi / k1  # 波长
         fai = float(self.textEdit_4.text()) * math.pi
         alpha = float(self.textEdit_3.text())
         n = 6  # 波形起始位置
         z = np.linspace(0,n * lambda1, 100)
      self.statusBar().showMessage("正在仿真....")
      # 时间循环
      t = np.linspace(0, 1.0, 100)
      for i in range(len(t)):
         if self.runorpause == 1:
            scale1 = self.voltsdial.value()
            self.labelmag.setText('x'+str(scale1))
            scale2 = self.timedial.value() / 10
            self.labelelec.setText('x'+str(scale2))
            # 电场
            E1 = np.exp(-alpha*z) * Ei0 * np.cos(omiga * t[i] - k1 * z) * scale2 # 电场公式
            # 磁场
            H1 = np.exp(-alpha*z) * Ei0 / eta1 * np.cos(omiga * t[i] - k1 * z-fai) * scale1  # 磁场公式
            # 绘制
            if self.comboBox.currentText() == '单独显示':       # 电场和磁场独立显示
               #self.label_2D_E_2.show()
               self.label_2D_H_2.show()
               self.label_2D_E_3.hide()
               self.m.plot(z,E1,H1,n*lambda1)
               
               QtWidgets.QApplication.processEvents()
            if self.comboBox.currentText() == '合并显示':               # # 电场和磁场合并显示
               #self.label_2D_E_2.hide()
               self.label_2D_H_2.hide()
               self.label_2D_E_3.show()
               self.n.plot(z,E1,H1,n*lambda1)
            
               QtWidgets.QApplication.processEvents()
            # 绘制3D
            self.n3D.plot3D(z,E1,H1,n*lambda1)
            QtWidgets.QApplication.processEvents()
         else:
            while(1):
               scale1 = self.voltsdial.value()
               self.labelmag.setText('x'+str(scale1))
               scale2 = self.timedial.value() / 10
               self.labelelec.setText('x'+str(scale2))
               # 电场
               E1 = np.exp(-alpha*z) * Ei0 * np.cos(omiga * t[i] - k1 * z) * scale2 # 电场公式
               # 磁场
               H1 = np.exp(-alpha*z) * Ei0 / eta1 * np.cos(omiga * t[i] - k1 * z-fai) * scale1  # 磁场公式
               # 绘制
               if self.comboBox.currentText() == '单独显示':       # 电场和磁场独立显示
                  #self.label_2D_E_2.show()
                  self.label_2D_H_2.show()
                  self.label_2D_E_3.hide()
                  self.m.plot(z,E1,H1,n*lambda1)
                  
                  QtWidgets.QApplication.processEvents()
               if self.comboBox.currentText() == '合并显示':               # # 电场和磁场合并显示
                  #self.label_2D_E_2.hide()
                  self.label_2D_H_2.hide()
                  self.label_2D_E_3.show()
                  self.n.plot(z,E1,H1,n*lambda1)
               
                  QtWidgets.QApplication.processEvents()
               # 绘制3D
               self.n3D.plot3D(z,E1,H1,n*lambda1)
               if self.runorpause == 1:
                  break
               QtWidgets.QApplication.processEvents()
      self.statusBar().showMessage("仿真结束",3000)
         
if __name__ == "__main__":
   app = QtWidgets.QApplication(sys.argv)  
   window = mywindow()

   window.show()                       
   sys.exit(app.exec_())                   
