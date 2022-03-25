# -*- coding: utf-8 -*-
from pickle import TRUE
from tkinter import image_names
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from field import Ui_MainWindow as UIM
from infordia import Ui_InforDialog as DIA

import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

class mywindow(QtWidgets.QMainWindow,UIM):
   def __init__(self):
      super(mywindow, self).__init__()
      self.setupUi(self)
      self.pushButton.clicked.connect(self.openimage)
      self.ch1Button.clicked.connect(self.change)
      self.actionInformation.triggered.connect(self.infodis)

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
      t = np.linspace(0, 0.1, 100)
      plt.figure(figsize=(8,3.5))
      for i in range(len(t)):
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
            self.label_2D_E_2.show()
            self.label_2D_H_2.show()
            self.label_2D_E_3.hide()
            # 电场画图
            
            plt.plot(z, E1, color='blue', alpha=0.5)
            plt.fill_between(z, 0, E1, color='blue', alpha=.25)  # 填充两个函数之间的区域，本例中填充（0和Y+1之间的区域）
            plt.xlim(0,n * lambda1)
            plt.ylim(-1.5, 1.5)
            #plt.xlabel('Spatial location')
            plt.ylabel('Electric field strength')
            #plt.title('Vertical incidence of plane wave on ideal conductor -- electric field')
            filename_E_2D = './results_E/E_time=' + str(t[i]) + '.png'
            plt.savefig(filename_E_2D)
            plt.clf()

            # 磁场画图
            plt.plot(z, H1, color='red', alpha=0.5)
            plt.fill_between(z, 0, H1, color='red', alpha=.25)  # 填充两个函数之间的区域，本例中填充（0和Y+1之间的区域）
            plt.xlim(0,n * lambda1)
            # plt.ylim(-0.01*scale, 0.01*scale)
            plt.ylim(-1.5, 1.5)                         # 统一坐标轴，便于合并前后的流畅
            #plt.xlabel('Spatial location')
            plt.ylabel('Magnetic induction')
            #plt.title('Vertical incidence of plane wave on ideal conductor -- magnetic field')
            filename_H_2D = './results_H/H_time=' + str(t[i]) + '.png'
            plt.savefig(filename_H_2D)
            plt.clf()

            # 利用qlabel显示图片
            png_E = QtGui.QPixmap(filename_E_2D)
            self.label_2D_E_2.setPixmap(png_E)
            QtWidgets.QApplication.processEvents()

            png_H = QtGui.QPixmap(filename_H_2D)
            self.label_2D_H_2.setPixmap(png_H)
            QtWidgets.QApplication.processEvents()
         if self.comboBox.currentText() == '合并显示':               # # 电场和磁场合并显示
            self.label_2D_E_2.hide()
            self.label_2D_H_2.hide()
            self.label_2D_E_3.show()

            # 电场
            plt.figure(figsize=(8,5))
            plt.plot(z, E1, color='blue', alpha=0.5)
            plt.fill_between(z, 0, E1, color='blue', alpha=.25)  # 填充两个函数之间的区域，本例中填充（0和Y+1之间的区域）

            # 磁场
            plt.plot(z, H1, color='red', alpha=0.5)
            plt.fill_between(z, 0, H1, color='red', alpha=.25)  # 填充两个函数之间的区域，本例中填充（0和Y+1之间的区域）
            plt.xlim(0,n * lambda1)
            plt.ylim(-2, 2)
            plt.xlabel('Spatial location')
            plt.ylabel('Electric and Magnetic field strength')
            plt.title('Vertical incidence of plane wave on ideal conductor')
            filename_EH_2D = './results_E+H_2D/E+H_2D_time=' + str(t[i]) + '.png'
            plt.savefig(filename_EH_2D)
            plt.close()

            # 利用qlabel显示图片
            png_E = QtGui.QPixmap(filename_EH_2D)
            self.label_2D_E_3.setPixmap(png_E)
            QtWidgets.QApplication.processEvents()
         # 绘制3D
         fig = plt.figure()
         ax = fig.gca(projection='3d')
         figure1 = ax.plot3D(E1, np.zeros_like(E1), z, c='b')
         figure2 = ax.plot3D(np.zeros_like(H1), H1, z, c='r')
         #plt.xlim(-2, 2)
         #plt.ylim(-0.01*scale1, 0.01*scale1)
         plt.xlabel('Electric field x')
         plt.ylabel('Magnetic field y')
         plt.title('Vertical incidence of plane wave on ideal conductor')
         filename_EH_3D = './results_E+H_3D/E+H_3D_time=' + str(t[i]) + '.png'
         plt.savefig(filename_EH_3D)
         plt.close()
         # 利用qlabel显示图片
         png_EH_3D = QtGui.QPixmap(filename_EH_3D)
         self.label_3D_EH.setPixmap(png_EH_3D)
         QtWidgets.QApplication.processEvents()
      self.statusBar().showMessage("仿真结束",3000)

if __name__ == "__main__":
   app = QtWidgets.QApplication(sys.argv)  
   window = mywindow()

   window.show()                       
   sys.exit(app.exec_())                   
