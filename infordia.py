# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infordia.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InforDialog(object):
    def setupUi(self, InforDialog):
        InforDialog.setObjectName("InforDialog")
        InforDialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(InforDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(InforDialog)
        self.label.setGeometry(QtCore.QRect(150, 0, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Harlow Solid Italic")
        font.setPointSize(14)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(InforDialog)
        self.textBrowser.setGeometry(QtCore.QRect(60, 40, 280, 192))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(InforDialog)
        self.buttonBox.accepted.connect(InforDialog.accept)
        self.buttonBox.rejected.connect(InforDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InforDialog)

    def retranslateUi(self, InforDialog):
        _translate = QtCore.QCoreApplication.translate
        InforDialog.setWindowTitle(_translate("InforDialog", "Dialog"))
        self.label.setText(_translate("InforDialog", "MyAPP"))
        self.textBrowser.setHtml(_translate("InforDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">基于PyQT开发的电磁场仿真软件。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">v1.0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">基础功能编写。根据参数显示传播波形。                                    </p>\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">电信1901 毛睿</p>\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">     2022/3</p></body></html>"))

