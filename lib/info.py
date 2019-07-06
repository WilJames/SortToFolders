# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info.ui',
# licensing of 'info.ui' applies.
#
# Created: Sat Jul  6 16:02:34 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_info(object):
    def setupUi(self, info):
        info.setObjectName("info")
        info.resize(496, 356)
        self.gridLayout = QtWidgets.QGridLayout(info)
        self.gridLayout.setContentsMargins(5, 0, 1, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(info)
        self.textBrowser.setStyleSheet("")
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(info)
        QtCore.QMetaObject.connectSlotsByName(info)

    def retranslateUi(self, info):
        info.setWindowTitle(QtWidgets.QApplication.translate("info", " ", None, -1))
        self.textBrowser.setHtml(QtWidgets.QApplication.translate("info", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                                  "p, li { white-space: pre-wrap; }\n"
                                                                  "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                                  "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Tahoma\'; font-size:8pt;\"><br /></p></body></html>", None, -1))
