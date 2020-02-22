# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QIcon, QFont
from PySide2.QtCore import (Qt, QUrl, Signal, QSize)

from time import time, strftime, gmtime, monotonic
from pathlib import Path, PurePath
import re
import os

from ui.copy_win import Ui_copy_win

_WINDOWS = os.name == 'nt'


class Copy_Win(QWidget):
    stopmovesignal = Signal()

    def __init__(self):
        super(Copy_Win, self).__init__()

        self.ui = Ui_copy_win()
        self.ui.setupUi(self)
        self.setFixedSize(368, 108)
        self.setWindowIcon(QIcon('assets/empty.png'))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.ui.label_5.setOpenExternalLinks(True)
        self.ui.widget.hide()
        # self.ui.pushButton.setText(u"\u2193")  # вниз
        self.ui.pushButton.setIcon(QIcon("assets/arrowD.png"))
        self.ui.pushButton.setIconSize(QSize(13, 13))
        # self.ui.label_dopinfo.setText('Подробнее')
        self.ui.pushButton.setText('Подробнее')

        self.ui.pushButton.clicked.connect(self.hideshowdopinfo)
        self.ui.pushButton_2.clicked.connect(self.stopmove)

        # self.ui.progressBar.setValue(55)

    def stopmove(self):
        self.stopmovesignal.emit()
        # self.MovingThread.status_run = False

    def hideshowdopinfo(self):
        if self.ui.widget.isVisible():
            self.ui.widget.hide()
            # self.ui.pushButton.setText(u"\u2193")  # вниз
            self.ui.pushButton.setIcon(QIcon("assets/arrowD.png"))
            self.ui.pushButton.setIconSize(QSize(13, 13))
            # self.ui.label_dopinfo.setText('Подробнее')
            self.ui.pushButton.setText('Подробнее')
            self.setFixedSize(368, 108)
        else:
            self.ui.widget.show()
            # self.ui.pushButton.setText(u"\u2191")  # вверх
            self.ui.pushButton.setIcon(QIcon("assets/arrowU.png"))
            self.ui.pushButton.setIconSize(QSize(13, 13))
            # self.ui.label_dopinfo.setText('Меньше сведений')
            self.ui.pushButton.setText('Меньше сведений')
            self.setFixedSize(368, 224)

    def showWin(self, total_files, total_size):
        total_files = total_files
        total_size = total_size

        # Блок всего
        self.ui.label_10.setText('Файлов:')
        self.ui.label_14.setText(str(total_files))

        self.ui.label_11.setText('Размер:')
        self.ui.label_15.setText(self.humansize(total_size))

        self.ui.progressBar.setValue(0)
        self.ui.widget.hide()
        self.setFixedSize(368, 108)

        self.show()

    def progress(self, progressDict):
        time_remain = progressDict['time_remain']
        speed = f"{self.humansize(progressDict['speed'])}/s"
        percent = progressDict['percent']
        less_files = progressDict['less_files']
        less_size = progressDict['less_size']

        end_time = monotonic() - self.start_time
        if _WINDOWS:
            end_time = strftime('%#Hh %#Mm %#Ss', gmtime(end_time))
            time_remain = strftime('%#Hh %#Mm %#Ss', gmtime(time_remain))
        else:
            end_time = strftime('%-Hh %-Mm %-Ss', gmtime(end_time))
            time_remain = strftime('%-Hh %-Mm %-Ss', gmtime(time_remain))

        end_time = re.sub(r'0h\s|0m\s', '', end_time)
        time_remain = re.sub(r'0h\s|0m\s', '', time_remain)

        self.setWindowTitle(f'Выполнено: {percent}%')
        self.ui.label_4.setText(f'Скорость: {speed}')
        self.ui.progressBar.setValue(percent)
        self.ui.progressBar.setFormat(f'{less_files} | %p%')
        # Блок прошло всего
        self.ui.label_9.setText('Времени:')
        self.ui.label_13.setText(end_time)

        # Блок осталось
        self.ui.label_2.setText('Времени:')
        self.ui.label_6.setText(time_remain)

        self.ui.label_3.setText('Файлов:')
        self.ui.label_7.setText(str(less_files))

        self.ui.label_8.setText('Размер:')
        self.ui.label_12.setText(self.humansize(less_size))

    def setName(self, alist):
        pfrom = PurePath(alist[1]).parent
        pto = PurePath(alist[2]).parent
        namefrom = PurePath(pfrom).parts[-1]
        nameto = PurePath(pto).parts[-1]

        path1 = QUrl.fromLocalFile(f'{pfrom}').toString()
        path1 = f'''<a href='{path1}'>{namefrom}</a>'''

        path2 = QUrl.fromLocalFile(f'{pto}').toString()
        path2 = f'''<a href='{path2}'>{nameto}</a>'''

        self.ui.label_5.setText(f'Из {path1} в {path2}')
        self.ui.label.setText(f'Имя: {alist[0]}')
        # font1 = QFont()
        # font1.setPointSize(9)
        # self.ui.label.setFont(font1)

    def humansize(self, nbytes):
        ''' Перевод байт в кб, мб и т.д.'''
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        i = 0
        while nbytes >= 1024 and i < len(suffixes) - 1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])

    def starttimer(self):
        self.start_time = monotonic()
