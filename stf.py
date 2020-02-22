# -*- coding: utf-8 -*-
import json
import os
import re
# from time import time, strftime, gmtime, monotonic

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
                            QRect, QSize, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
                           QRadialGradient)
from PySide2.QtWidgets import *

from ui.mtf_ui import Ui_MainWindow
from ui.lang import Language
from forms.copy_win import Copy_Win
from threads.MovingThread import MovingThread
# from forms.info_form import Info


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setWindowTitle('Sort To Folders')

        self.MovingThread = MovingThread()
        self.CopyWin = Copy_Win()

        self.MovingThread.finished.connect(self.finish)
        self.MovingThread.showWindowProgress.connect(self.copyShow)
        self.MovingThread.progress.connect(self.progress)
        self.MovingThread.setName.connect(self.setName)
        self.CopyWin.stopmovesignal.connect(self.start)
        self.ui.lineEdit.setPlaceholderText('Добавить расширение')

        self.ui.tabWidget.currentChanged.connect(self.tabWidget)

        self.loading()

        # Кнопка добавить +
        self.ui.pushButton_3.clicked.connect(self.add)
        self.ui.pushButton_4.clicked.connect(self.delete)
        # Кнопка тест
        self.ui.pushbtest.clicked.connect(self.test2)
        self.ui.pushButton_6.clicked.connect(self.start)

        self.ui.tableWidget_3.setSortingEnabled(True)
        header = self.ui.tableWidget_3.horizontalHeader()
        header.sortIndicatorChanged.connect(self.sort)
        # print(self._dir(header_2))

        # self.test2()

        '''To Do
        -  Выбор языка и запись в файл
        -  Сделать файл языка
        '''

    def test2(self):
        self.CopyWin.showWin(12, 123, 55)

    def copyShow(self):
        totalFiles = self.MovingThread.totalFiles
        totalSize = self.MovingThread.totalSize

        self.CopyWin.showWin(totalFiles, totalSize)

    def progress(self, progressDict):
        self.CopyWin.progress(progressDict)

    def setName(self, namesList):
        self.CopyWin.setName(namesList)

    def _dir(self, widget):
        for i in dir(widget):
            print(i)

    def test(self):
        table = self.ui.tableWidget_2
        print(table.selectedRanges())

    def start(self):
        if not self.MovingThread.isRunning():
            dataTarget = [x for x in self.dataTarget if x['chekbox']
                          and os.path.exists(x['path'])]
            data = [x for x in self.data if x['chekbox']
                    and os.path.exists(x['path'])]

            if dataTarget and data:
                self.CopyWin.starttimer()
                self.ui.pushButton_6.setText('Стоп')
                self.MovingThread.st(dataTarget, data)
            else:
                self.ui.statusbar.showMessage('Нечего перемещать', 3000)
        else:
            self.MovingThread.statusWork = False

    def finish(self):
        self.ui.pushButton_6.setText('Старт')
        # добавить скрытие окна перемещения файлов

    def eventFilter(self, source, event):
        # print(event.type(), source)
        if event.type() == QEvent.Enter and source is self.ui.tableWidget_3:
            self.focusSet = True
        elif event.type() == QEvent.Leave and source is self.ui.tableWidget_3:
            self.focusSet = False
        # elif event.type() == QtCore.QEvent.FocusOut and (source is self.listWidget_categori or source is self.listWidget_extensions):
        #     self.focus_listwindget = 0
        return super(MainWindow, self).eventFilter(source, event)

    def getCurrent(self):
        if self.currentTab == 0:
            table = self.ui.tableWidget
            data = self.dataTarget

        elif self.currentTab == 1:
            table = self.ui.tableWidget_2
            data = self.data
        return table, data

    def doubleClicked(self, item):
        if (currentColumn:= item.column()) == 1:
            _, data = self.getCurrent()
            currentRow = item.row()
            pathChosen = QFileDialog.getExistingDirectory(
                self, 'Выбор папки', os.path.expanduser('~'))
            data[currentRow]['path'] = pathChosen

            if not data[currentRow]['name']:
                sep = os.path.sep + (os.path.altsep or '')
                name = os.path.basename(pathChosen.rstrip(sep))
                data[currentRow]['name'] = name

            self.fillingInTable()

    def editTable(self, item):
        _, data = self.getCurrent()

        currentRow = item.row()
        currentCol = item.column()

        if currentCol == 0:
            data[currentRow]['name'] = item.text()
            check = item.checkState()

            if check is Qt.CheckState.Checked:
                data[currentRow]['chekbox'] = True
            else:
                data[currentRow]['chekbox'] = False
        elif currentCol == 1:
            data[currentRow]['path'] = item.text()

    def keyPressEvent(self, event):
        ctrl = event.modifiers() == 0x04000000

        if ctrl and event.key() == 0x56:  # V key
            self.paste()
        elif (ctrl and event.key() == 0x01000007) and self.focusSet:
            self.deleteExt()
        elif ctrl and event.key() == 0x01000007:  # Delete key
            self.delete()
        elif event.key() == 0x01000007:  # Delete key
            self.clear()

    def openMenu(self, pos):
        menu = QMenu()
        if self.focusSet:
            # menu.addAction("Сортировать", self.sort)
            menu.addAction("Удалить", self.deleteExt)
            menu.addAction("Удалить всё", self.deleteExtAll)
        else:
            menu.addAction("Вставить", self.paste)
            menu.addAction("Очистить", self.clear)
            menu.addAction("Удалить", self.delete)
            menu.addAction("Удалить всё", self.deleteAll)

        menu.exec_(QCursor.pos())

    def sort(self, index, order):
        table, data = self.getCurrent()
        tableExt = self.ui.tableWidget_3

        if order is Qt.AscendingOrder:
            for i in data:
                i['extension'].sort()
        else:
            for i in data:
                i['extension'].sort(reverse=True)

        self.preloadExt()

    def clear(self):
        table, _ = self.getCurrent()

        currentRow = table.currentRow()
        currentCol = table.currentColumn()
        table.setItem(currentRow, currentCol, QTableWidgetItem(None))

    def paste(self):
        table, data = self.getCurrent()
        currentRow = table.currentRow()
        currentCol = table.currentColumn()
        clipboard = QApplication.clipboard().text()

        if currentCol == 1:
            clipboard = clipboard.replace('\\', '/')

            if not data[currentRow]['name']:
                sep = os.path.sep + (os.path.altsep or '')
                name = os.path.basename(clipboard.rstrip(sep))
                data[currentRow]['name'] = name

            data[currentRow]['path'] = clipboard
            data[currentRow]['chekbox'] = True

        elif currentCol == 0:
            data[currentRow]['name'] = clipboard

        self.fillingInTable()
        table.setCurrentCell(currentRow, currentCol)
        if self.currentTab == 1:
            self.preloadExt()

    def deleteExtAll(self):
        table, data = self.getCurrent()
        tableExt = self.ui.tableWidget_3

        ext = data[self.dataRowExt]['extension']
        ext.clear()
        self.preloadExt()

    def deleteExt(self):
        if self.dataRowExt >= 0:
            table, data = self.getCurrent()
            tableExt = self.ui.tableWidget_3

            ext = data[self.dataRowExt]['extension']
            if (items:= tableExt.selectedItems()):
                for item in items:
                    ext.remove(item.text())
            else:
                ext.pop()

        self.preloadExt()

    def delete(self):
        table, data = self.getCurrent()
        if (items:= table.selectedItems()):
            for index, item in enumerate(items):
                data.pop(item.row() - index)
        else:
            data.pop()

        self.fillingInTable()

    def deleteAll(self):
        table, data = self.getCurrent()
        data.clear()
        self.fillingInTable()

    def addExt(self):
        lineEdit = self.ui.lineEdit
        textList = lineEdit.text().strip().split()

        if self.dataRowExt >= 0:
            table, data = self.getCurrent()
            ext = data[self.dataRowExt]['extension']
            for i in textList:
                if i.startswith('.') and i not in ext:
                    ext.append(i)

            lineEdit.clear()

        self.preloadExt()

    def add(self):
        if self.currentTab == 0:  # вкладка откуда
            self.dataTarget.append({'name': '', 'path': '', 'chekbox': True})

        elif self.currentTab == 1:  # вкладка откуда
            self.data.append(
                {'name': '', 'path': '', 'extension': [], 'chekbox': True})

        self.fillingInTable()

    def normText(self, qstring):
        norm = re.compile(r'[^a-zA-Z0-9\.\s]+')
        space = re.compile(r'\s{2,}')
        lineEdit = self.ui.lineEdit
        qstring = norm.sub('', qstring)
        qstring = space.sub(' ', qstring.lower())
        lineEdit.setText(qstring)

    def tabWidget(self, index):
        self.currentTab = index
        if index == 0:  # вкладка откуда
            if self.ui.widget.isHidden():
                self.ui.widget.show()
            self.fillingInTable()
        elif index == 1:  # вкладка куда
            if self.ui.widget.isHidden():
                self.ui.widget.show()
            self.fillingInTable()
            self.preloadExt()
        elif index == 2:  # вкладка настройки
            self.ui.widget.hide()

    def _connect(self):
        # Первая вкладка
        self.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.openMenu)
        self.ui.tableWidget.itemDoubleClicked.connect(self.doubleClicked)
        # Вторая вкладка
        self.ui.tableWidget_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget_2.customContextMenuRequested.connect(self.openMenu)
        self.ui.tableWidget_2.itemDoubleClicked.connect(self.doubleClicked)
        self.ui.tableWidget_2.itemClicked.connect(self.preloadExt)
        # Вторая вкладка расширения
        self.ui.tableWidget_3.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget_3.customContextMenuRequested.connect(self.openMenu)
        self.ui.lineEdit.returnPressed.connect(self.addExt)
        self.ui.lineEdit.textChanged.connect(self.normText)
        self.ui.tableWidget_3.installEventFilter(self)

    def preloadExt(self, item=None):
        tableExt = self.ui.tableWidget_3
        table, data = self.getCurrent()

        tableExt.clear()
        tableExt.setColumnCount(1)
        tableExt.setRowCount(0)

        if (items:= table.selectedItems()):
            self.dataRowExt = items[-1].row()
            extensions = data[self.dataRowExt].get('extension')
            tableExt.setRowCount(len(extensions))

            for index, extension in enumerate(extensions):
                item = QTableWidgetItem(extension)
                item.setTextAlignment(0x0002)  # aligment to Right
                tableExt.setItem(index, 0, item)
        else:
            self.dataRowExt = -1

        tableExt.setHorizontalHeaderLabels(["Расширения"])
        tableExt.resizeColumnsToContents()

    def fillingInTable(self):
        table, data = self.getCurrent()
        try:
            table.itemChanged.disconnect(self.editTable)
        except:
            pass

        table.clear()
        table.setColumnCount(2)
        table.setRowCount(len(data))

        for index, dict_ in enumerate(data):
            path = QTableWidgetItem(dict_.get('path'))
            path.setFlags(Qt.ItemFlag(1 | 32))

            name = QTableWidgetItem(dict_.get('name'))
            if dict_.get('chekbox'):
                name.setCheckState(Qt.Checked)
            else:
                name.setCheckState(Qt.Unchecked)

            table.setItem(index, 0, name)
            table.setItem(index, 1, path)

        table.setHorizontalHeaderLabels(["Имя", "Путь"])
        table.resizeColumnsToContents()

        table.itemChanged.connect(self.editTable)

    def loading(self):
        self.currentTab = self.ui.tabWidget.currentIndex()

        for i, v in enumerate(['data', 'data_target', 'settings']):
            try:
                with open(f'settings/{v}.json', 'r', encoding="utf-8") as data:
                    if i == 0:
                        self.data = json.load(data)
                    elif i == 1:
                        self.dataTarget = json.load(data)
                    elif i == 2:
                        self.setting = json.load(data)
            except FileNotFoundError:
                if i == 0:
                    self.data = []
                elif i == 1:
                    self.dataTarget = []
                elif i == 2:
                    self.setting = {}

        size = self.setting.get('mainwindowsize', [715, 505])
        self.resize(*size)

        lang = self.setting.get('lang')
        self.lang = Language(lang)


        self.focusSet = False
        tableExt = self.ui.tableWidget_3
        tableExt.setColumnCount(1)
        tableExt.horizontalHeader().setVisible(True)
        tableExt.setHorizontalHeaderLabels(["Расширения"])
        tableExt.setRowCount(0)

        self.fillingInTable()
        self._connect()
        self.dataRowExt = -1

    def closeEvent(self, event):
        if self.MovingThread.isRunning():
            self.ui.statusBar.showMessage('Запущен процесс перемещения', 3000)
            event.ignore()
        else:
            with open('settings/data.json', 'w', encoding="utf-8") as data, open('settings/data_target.json', 'w', encoding="utf-8") as dataTarget:
                json.dump(self.data, data, indent=4, ensure_ascii=False)
                json.dump(self.dataTarget, dataTarget,
                          indent=4, ensure_ascii=False)

            with open('settings/settings.json', 'w', encoding="utf-8") as f:
                self.settings = {'lang': 'ru',
                                 'mainwindowsize': [self.width(), self.height()]}
                json.dump(self.settings, f, indent=4, ensure_ascii=False)


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса myApp
    theme = QDarkPalette()
    theme.set_app(app)

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    import sys
    from theme.DarkPalette import QDarkPalette
    main()  # то запускаем функцию main()
