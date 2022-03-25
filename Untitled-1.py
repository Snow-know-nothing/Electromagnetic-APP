# -*- coding: utf-8 -*-

"""

-------------------------------------------------

@File：PyQt_文本校验器.py

@Desc :

@Version：V 1.0.0

@Author： Maxson King

-------------------------------------------------

"""

#模块导入

import sys

from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *

# 业务逻辑类方法

class LineEditValidator(QWidget):



    def __init__(self, parent = None):

        super(LineEditValidator,self).__init__(parent)

        # 设置属性

        self.setWindowTitle('文本校验器')

        self.resize(500, 300)

        self.setupUI1()

        # 业务逻辑方法

    def setupUI1(self):



        formlayout = QFormLayout()

        intLe = QLineEdit()

        doubleLe = QLineEdit()

        validatorLe = QLineEdit()

        formlayout.addRow('整数类型',intLe)

        formlayout.addRow('浮点类型',doubleLe)

        formlayout.addRow('数字与字母',validatorLe)

        intLe.setPlaceholderText('整型')

        doubleLe.setPlaceholderText('浮点型')

        validatorLe.setPlaceholderText('字母和小数')

        # 整数校验器 [1,99]

        intValidator = QIntValidator(self)

        intValidator.setRange(1,99)

        # 浮点校验器 [-360,360]，精度：小数点后2位

        doubleValidator = QDoubleValidator(self)

        doubleValidator.setRange(-360,360)

        doubleValidator.setNotation(QDoubleValidator.StandardNotation)

        # 设置精度，小数点2位

        doubleValidator.setDecimals(2)

        # 字符和数字

        reg = QRegExp('[a-zA-z0-9]+$')

        validator = QRegExpValidator(self)

        validator.setRegExp(reg)

        # 设置校验器

        intLe.setValidator(intValidator)

        doubleLe.setValidator(doubleValidator)

        validatorLe.setValidator(validator)

        self.setLayout(formlayout)

if __name__ == '__main__':

    # 创建应用程序实例

    app = QApplication(sys.argv)

    # 展示控件

    window = LineEditValidator()

    window.show()

    # 应用程序的执行, 进入到消息循环

    sys.exit(app.exec_())