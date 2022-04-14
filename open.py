# -*- coding: utf-8 -*-
#from pickle import TRUE
#from tkinter import image_names
from cmath import sqrt
from pickle import FALSE
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os

from sqlalchemy import true
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
      self.comboBox_2.currentIndexChanged.connect(self.labchange)
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

      self.radioButton.hide()
      self.ch1Button.show()

   def labchange(self):
      if self.comboBox_2.currentText() == "实验一、介质中传播":
         self.spinBox.setEnabled(False)
         self.spinBox_2.setEnabled(False)
         self.spinBox_3.setEnabled(False)
         self.spinBox_4.setEnabled(False)
         self.radioButton.hide()
         self.ch1Button.show()
         self.ch1Button.setText("导电介质")
         self.radioButton.setText("理想介质")
         self.labelcommand.setText("电场幅度(V/m)")
         self.label_2.setText("角频率(*2π rad/s)")
         self.label_5.setText("衰减常数")
         self.label_6.setText("相位差(*π)")
         self.label_7.setText( "复波阻抗模值(*π)")
      elif self.comboBox_2.currentText() == "实验二、入射反射及透射":
         self.spinBox.setEnabled(True)
         self.spinBox_2.setEnabled(True)
         self.spinBox_3.setEnabled(True)
         self.spinBox_4.setEnabled(True)
         self.radioButton.show()
         self.ch1Button.hide()
         self.ch1Button.setText("导电介质")
         self.radioButton.setText("理想介质")
         self.textEdit_3.setDisabled(True)
         self.textEdit_4.setDisabled(True)
         self.textEdit_5.setDisabled(True)
         self.labelcommand.setText("电场幅度(V/m)")
         self.label_2.setText("角频率(*2π rad/s)")
         self.label_5.setText("") 
         self.label_6.setText("")
         self.label_7.setText("")
      elif self.comboBox_2.currentText() == "实验三、波导传播":
         self.radioButton.show()
         self.ch1Button.show()
         self.labelcommand.setText("切片位置t")
         self.label_2.setText("切片时间z")
         self.label_5.setText("") 
         self.label_6.setText("")
         self.label_7.setText("")
         self.ch1Button.setText("波导电场")
         self.radioButton.setText("波导磁场")
         self.radioButton.setEnabled(True)
         self.ch1Button.setEnabled(True)
         self.spinBox.setEnabled(False)
         self.spinBox_2.setEnabled(False)
         self.spinBox_3.setEnabled(False)
         self.spinBox_4.setEnabled(False)
         self.textEdit_3.setDisabled(True)
         self.textEdit_4.setDisabled(True)
         self.textEdit_5.setDisabled(True)


   def saveit(self):
      fileNamebase, filetype = QtWidgets.QFileDialog.getSaveFileName(self,  
                                    "文件保存",  
                                    self.cwd, # 起始路径 
                                    "All Files (*);;PNG Files (*.png)")  

      if fileNamebase == "":
            print("\n取消选择")
            return
      filename = fileNamebase[0:-4] + '1' + '.png'
      #img = self.label_2D_H_2.pixmap().toImage()
      self.m.figure.savefig(filename)
      filename = fileNamebase[0:-4] + '2' + '.png'
      self.n.figure.savefig(filename)
      filename = fileNamebase[0:-4] + '3' + '.png'
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

      if self.comboBox_2.currentText() == "实验一、介质中传播":
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
               x,y = np.meshgrid(10,10)
               self.n3D.plot3D(x,y,z,E1,H1,n*lambda1)
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
                  x,y = np.meshgrid(10,10)
                  self.n3D.plot3D(x,y,z,E1,H1,n*lambda1)
                  if self.runorpause == 1:
                     break
                  QtWidgets.QApplication.processEvents()
      elif self.comboBox_2.currentText() == "实验二、入射反射及透射":
         # 参数设置
         if (self.radioButton.isChecked( ) == False):
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
            z = np.linspace(-n * lambda1, 0, 100)
         else:
         # 计算参数
                     # 计算参数
            u0 = 4 * math.pi * pow(10, -7)  # 真空中介电常数
            e0 = 1 / (36 * math.pi) * pow(10, -9)  # 真空中磁导率
            # 介质1的介电常数和磁导率
            u1 = u0 * self.spinBox.value()
            e1 = e0 * self.spinBox_2.value()
            # 介质2的介电常数和磁导率
            u2 = u0 * self.spinBox_4.value()
            e2 = e0 * self.spinBox_3.value()
            omiga = omiga = float(self.textEdit_2.text()) *2* math.pi  # 频率
            k1 = omiga * math.sqrt(u1 * e1)  # 波数k1
            k2 = omiga * math.sqrt(u2 * e2)  # 波数k2
            eta1 = math.sqrt(u1 / e1)  # 复波阻抗eta1
            eta2 = math.sqrt(u2 / e2)  # 复波阻抗eta2
            Ei0 = float(self.textEdit.text())  # 初始场强
            lambda1 = 2 * math.pi / k1  # 波长
            n = 2  # 波形起始位置
            z1 = np.linspace(-n * lambda1, 0, 100)
            z2 = np.linspace(0, n * lambda1, 100)
            z = np.append(z1, z2)
            R = (eta2 - eta1) / (eta2 + eta1)  # 反射系数
            T = 2 * eta2 / (eta2 + eta1)  # 透射系数
            
         self.statusBar().showMessage("正在仿真....")
         # 时间循环
         t = np.linspace(0, 1.0, 100)
         for i in range(len(t)):
            if self.runorpause == 1:
               scale1 = self.voltsdial.value()
               self.labelmag.setText('x'+str(scale1))
               scale2 = self.timedial.value() / 10
               self.labelelec.setText('x'+str(scale2))
                  # 参数设置
               if (self.radioButton.isChecked( ) == False):
                  # 电场
                  E1 = 2 * Ei0 *  np.sin(k1 * z) * np.sin(omiga * t[i]) * scale2 # 电场公式
                  # 磁场
                  H1 = 2 * Ei0 / eta1 * np.cos(k1 * z) * np.cos(omiga * t[i]) * scale1  # 磁场公式
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
                  x,y = np.meshgrid(10,10)
                  self.n3D.plot3D(x,y,z,E1,H1,n*lambda1)
                  QtWidgets.QApplication.processEvents()
               else:
               # 计算参数
                  E1 = Ei0 * (np.cos(omiga * t[i] - k1 * z1) + R * np.cos(omiga * t[i] + k1 * z1))  # 电场公式
                  E2 = T * Ei0 * np.cos(omiga * t[i] - k2 * z2)
                  E = scale2 * np.append(E1, E2)
                  # 介质1、2磁场
                  H1 = Ei0 / eta1 * (np.cos(omiga * t[i] - k1 * z1) - R * np.cos(omiga * t[i] + k1 * z1))  # 磁场公式
                  H2 = T * Ei0 / eta2 * np.cos(omiga * t[i] - k2 * z2)
                  # scale = 100
                  H = scale1 * np.append(H1, H2)
                  if self.comboBox.currentText() == '单独显示':       # 电场和磁场独立显示
                     #self.label_2D_E_2.show()
                     self.label_2D_H_2.show()
                     self.label_2D_E_3.hide()
                     self.m.plot(z,E,H,n*lambda1)
                     
                     QtWidgets.QApplication.processEvents()
                  if self.comboBox.currentText() == '合并显示':               # # 电场和磁场合并显示
                     #self.label_2D_E_2.hide()
                     self.label_2D_H_2.hide()
                     self.label_2D_E_3.show()
                     self.n.plot(z,E,H,n*lambda1)
                  
                     QtWidgets.QApplication.processEvents()
                  # 绘制3D
                  x,y = np.meshgrid(10,10)
                  self.n3D.plot3D(x,y,z,E,H,n*lambda1)
                  QtWidgets.QApplication.processEvents()
            else:
               while(1):
                  scale1 = self.voltsdial.value()
                  self.labelmag.setText('x'+str(scale1))
                  scale2 = self.timedial.value() / 10
                  self.labelelec.setText('x'+str(scale2))
                     # 参数设置
                  if (self.radioButton.isChecked( ) == False):
                     # 电场
                     E1 = 2 * Ei0 *  np.sin(k1 * z) * np.sin(omiga * t[i]) * scale2 # 电场公式
                     # 磁场
                     H1 = 2 * Ei0 / eta1 * np.cos(k1 * z) * np.cos(omiga * t[i]) * scale1  # 磁场公式
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
                     x,y = np.meshgrid(10,10)
                     self.n3D.plot3D(x,y,z,E1,H1,n*lambda1)
                     QtWidgets.QApplication.processEvents()
                  else:
                  # 计算参数
                     E1 = Ei0 * (np.cos(omiga * t[i] - k1 * z1) + R * np.cos(omiga * t[i] + k1 * z1))  # 电场公式
                     E2 = T * Ei0 * np.cos(omiga * t[i] - k2 * z2)
                     E = scale2 * np.append(E1, E2)
                     # 介质1、2磁场
                     H1 = Ei0 / eta1 * (np.cos(omiga * t[i] - k1 * z1) - R * np.cos(omiga * t[i] + k1 * z1))  # 磁场公式
                     H2 = T * Ei0 / eta2 * np.cos(omiga * t[i] - k2 * z2)
                     # scale = 100
                     H = scale1 * np.append(H1, H2)
                     if self.comboBox.currentText() == '单独显示':       # 电场和磁场独立显示
                        self.label_2D_H_2.show()
                        self.label_2D_E_3.hide()
                        self.m.plot(z,E,H,n*lambda1)
                        
                        QtWidgets.QApplication.processEvents()
                     if self.comboBox.currentText() == '合并显示':               # # 电场和磁场合并显示
                        #self.label_2D_E_2.hide()
                        self.label_2D_H_2.hide()
                        self.label_2D_E_3.show()
                        self.n.plot(z,E,H,n*lambda1)

                        QtWidgets.QApplication.processEvents()
                     # 绘制3D
                     x,y = np.meshgrid(10,10)
                     self.n3D.plot3D(x,y,z,E,H,n*lambda1)
                     QtWidgets.QApplication.processEvents()
                  if self.runorpause == 1:
                     break
                  #QtWidgets.QApplication.processEvents()  
      elif self.comboBox_2.currentText() == "实验三、波导传播":
         # 参数设置
         if (True):
            # 计算参数
            ao = 22.86
            bo = 10.16
            d  = 15
            H0 = 1
            f  = 9.375 * pow(10, 9)

            a=ao/1000
            b=bo/1000
            lc=2*a    
            l0=(3*pow(10, 8))/f
            u=4*math.pi*pow(10, -7)
            t = np.linspace(0,10,60)/(3*pow(10, 8))

            lg=l0/(math.sqrt(1-pow((l0/lc),2)))
            c=lg
            B=2*math.pi/lg
            w=2*math.pi*f
            x=np.linspace(0,a,d)
            y=np.linspace(0,b,d)
            z=np.linspace(0,c,d)
   
         self.statusBar().showMessage("正在仿真....")
         self.n3D.axes.set_box_aspect((c,a,b))
         self.n3D.axes.set_title('波导中的电磁场')
         # 时间循环
         #t = np.linspace(0, 1.0, 100)
         self.label_2D_H_2.hide()
         self.label_2D_E_3.show()
         t2 = float(self.textEdit.text())
         z2 = float(self.textEdit_2.text())
          #电场切片
         self.n.ax1.cla()
         ey2=w*u*a*H0*np.sin((np.pi/a)*x)*np.sin(w*t2-B*z2)/np.pi
         self.n.ax1.plot(x, ey2, color='blue', alpha=0.5)
         self.n.draw()
         for i in range(len(t)):
            if self.runorpause == 1:
               #三维作图
               x1,y1,z1= np.meshgrid(x,y,z) 
               ex=np.zeros_like(x1)
               ey=w*u*a*H0*np.sin((np.pi/a)*x1)*np.sin(w*t[i]-B*z1)/np.pi
               ez=np.zeros_like(x1)

               hy=np.zeros_like(x1)
               hx=B*a*H0*np.sin((np.pi/a)*x1)*(-np.sin(w*t[i]-B*z1))/np.pi
               hz=H0*np.cos((np.pi/a)*x1)*np.cos(w*t[i]-B*z1)

               self.n3D.axes.cla()
               #self.n3D.axes.set_box_aspect((c,a,b))
               if(self.ch1Button.isChecked() == True):
                  self.n3D.axes.quiver(z1,x1,y1,ez,ex,ey,color='red',length=0.0008, normalize=True)
               if(self.radioButton.isChecked() == True):
                  self.n3D.axes.quiver(z1,x1,y1,hz,hx,hy,color='blue',length=0.0008, normalize=True)

               self.n3D.draw()
               #title('波导管内电场分布图')
               # 绘制3D
               #x,y = np.meshgrid(10,10)
               #self.n3D.plot3D(z,E1,H1,n*lambda1)
               QtWidgets.QApplication.processEvents()
         
      self.statusBar().showMessage("仿真结束",3000)
         
if __name__ == "__main__":
   app = QtWidgets.QApplication(sys.argv)  
   window = mywindow()

   window.show()                       
   sys.exit(app.exec_())                   
