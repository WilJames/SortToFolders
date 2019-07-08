# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'finish.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_finish(object):
    def setupUi(self, finish):
        finish.setObjectName("finish")
        finish.resize(131, 111)
        self.verticalLayout = QtWidgets.QVBoxLayout(finish)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(finish)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_2 = QtWidgets.QPushButton(finish)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(finish)
        QtCore.QMetaObject.connectSlotsByName(finish)

    def retranslateUi(self, finish):
        _translate = QtCore.QCoreApplication.translate
        finish.setWindowTitle(_translate("finish", " "))
        self.pushButton_2.setText(_translate("finish", "Ok"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    finish = QtWidgets.QDialog()
    ui = Ui_finish()
    ui.setupUi(finish)
    finish.show()
    sys.exit(app.exec_())
