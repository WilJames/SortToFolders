# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'copy_win.ui'
##
# Created by: Qt User Interface Compiler version 5.14.1
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
                            QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
                           QRadialGradient)
from PySide2.QtWidgets import *


class Ui_copy_win(object):
    def setupUi(self, Ui_copy_win):
        if Ui_copy_win.objectName():
            Ui_copy_win.setObjectName(u"Ui_copy_win")
        Ui_copy_win.resize(368, 218)
        self.verticalLayout = QVBoxLayout(Ui_copy_win)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Ui_copy_win)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.label_5 = QLabel(Ui_copy_win)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAcceptDrops(False)

        self.verticalLayout.addWidget(self.label_5)

        self.progressBar = QProgressBar(Ui_copy_win)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setLayoutDirection(Qt.LeftToRight)
        self.progressBar.setValue(0)
        self.progressBar.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.progressBar)

        self.widget = QWidget(Ui_copy_win)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_5 = QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 9, -1, 9)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_5.addWidget(self.label_8)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_12)

        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setAlignment(Qt.AlignCenter)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_6.addWidget(self.label_9)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_13)

        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_7.addWidget(self.label_10)

        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_14)

        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_8.addWidget(self.label_11)

        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_15)

        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.verticalLayout.addWidget(self.widget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(Ui_copy_win)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(22, 22))
        self.pushButton.setMaximumSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.pushButton)

        self.label_dopinfo = QLabel(Ui_copy_win)
        self.label_dopinfo.setObjectName(u"label_dopinfo")

        self.horizontalLayout.addWidget(self.label_dopinfo)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_2 = QPushButton(Ui_copy_win)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(22, 22))
        self.pushButton_2.setMaximumSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Ui_copy_win)

        QMetaObject.connectSlotsByName(Ui_copy_win)
    # setupUi

    def retranslateUi(self, Ui_copy_win):
        Ui_copy_win.setWindowTitle(
            QCoreApplication.translate("Ui_copy_win", u"Form", None))
        self.label.setText(QCoreApplication.translate(
            "Ui_copy_win", u"\u0418\u043c\u044f:", None))
        self.label_5.setText(QCoreApplication.translate(
            "Ui_copy_win", u"\u0418\u0437 ... \u0432 ...", None))
        self.label_4.setText(QCoreApplication.translate(
            "Ui_copy_win", u"\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c:", None))
        self.groupBox.setTitle(QCoreApplication.translate(
            "Ui_copy_win", u"\u041e\u0441\u0442\u0430\u043b\u043e\u0441\u044c", None))
        self.label_2.setText(QCoreApplication.translate(
            "Ui_copy_win", u"\u0412\u0440\u0435\u043c\u0435\u043d\u0438:", None))
        self.label_6.setText("")
        self.label_3.setText(QCoreApplication.translate(
            "Ui_copy_win", u"\u0424\u0430\u0439\u043b\u043e\u0432:", None))
        self.label_7.setText("")
        self.label_8.setText(QCoreApplication.translate(
            "Ui_copy_win", u"\u0420\u0430\u0437\u043c\u0435\u0440:", None))
        self.label_12.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate(
            "Ui_copy_win", u"\u0412\u0441\u0435\u0433\u043e", None))
        self.label_9.setText(QCoreApplication.translate(
            "Ui_copy_win", u"\u0412\u0440\u0435\u043c\u0435\u043d\u0438:", None))
        self.label_13.setText("")
        self.label_10.setText(QCoreApplication.translate(
            "Ui_copy_win", u"\u0424\u0430\u0439\u043b\u043e\u0432:", None))
        self.label_14.setText("")
        self.label_11.setText(QCoreApplication.translate(
            "Ui_copy_win", u"\u0420\u0430\u0437\u043c\u0435\u0440:", None))
        self.label_15.setText("")
        self.pushButton.setText("")
        self.label_dopinfo.setText("")
        self.pushButton_2.setText(
            QCoreApplication.translate("Ui_copy_win", u"X", None))
    # retranslateUi
