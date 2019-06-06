from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtGui import QColor, QPalette, QIcon
# from PyQt5.QtCore import Qt
from sys import argv
from shutil import move
# from pickle import dump, load
from re import search
from time import time, sleep

import sort
import os
import json

# import re
# import pickle
# import shutil
# import sys
# import time
breaking = False
starting = False
win_size = 0
path = ''
dict_all = {}


class MyThread(QtCore.QThread, QtCore.QObject):
    info_not_files = QtCore.pyqtSignal()
    buttons_stop_text = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(float)

    def __init__(self):
        super().__init__()

    def run(self):
        global list_files, list_files2, breaking, starting
        size = 0
        counts = 0
        list_files = []
        list_files2 = []
        start_time = time()
        files = self.parsing_listdir()
        for cat in dict_all.keys():
            if cat != 'Global_path':
                put, extensions = self.parsing_dict(cat)
                if put != None:
                    names = self.parsing_rash(extensions, files)
                    self.check(put, names)

        all_count = len(list_files)
        if len(list_files) > 0:
            self.buttons_stop_text.emit()
            for i, (k, v) in enumerate(list_files):
                if breaking == True:
                    breaking = False
                    break
                elif breaking == False:
                    procent = round((i + 1) * 100 / all_count, 1)
                    self.progress.emit(procent)
                    size += os.path.getsize(k)
                    counts = i + 1
                    move(k, v)

            real_size = f'{size_text} {self.humansize(size)}'
            count = f'{files_count} {counts}'
            list_files.clear()
            list_files2.clear()
            end_time = round(time() - start_time)
            minutes = int(end_time // 60)
            seconds = int(end_time % 60)
            if minutes == 0:
                self.finished.emit(f'{time_text} {seconds} {seconds_text}\n{count}\n{real_size}')
            elif minutes > 0:
                self.finished.emit(f'{time_text} {minutes} {minutes_text} {seconds} {seconds_text}\n{count}\n{real_size}')
        elif len(list_files) == 0:
            self.info_not_files.emit()
            # 'здесь будет оповещение о том что нет файлов для перемещения'
        starting = False

    def humansize(self, nbytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        i = 0
        while nbytes >= 1024 and i < len(suffixes)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])

    # парсинг файлов в целевой папке
    def parsing_listdir(self):
        files = []
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    files.append(os.fsdecode(entry.name))
        return files

    # пасинг словаря для получения пути и расширений для категории
    def parsing_dict(self, category):
        # if category != 'Global_path':
        dict_cat = dict_all.get(category)
        put = dict_cat.get('put')
        if put != '' and put != path and os.path.exists(put):
            rash = dict_cat.get('rash')
            return put, rash
        else:
            return None, None

# парсинг расширений и соответсвия им файлам
    def parsing_rash(self, extensions, files):
        names = []
        for extension in extensions:
            for name in files:
                if name.endswith(extension):
                    names.append(name)
        return names

# переименование файла если такое имя есть в папке для перемещения
    def rename_copy(self, name_file, list_move_to_path):
        while name_file in list_move_to_path or name_file in list_files2:
            filename, extension = os.path.splitext(name_file)
            name_split = search(fr'(\()(\d*)(\){extension})', name_file)
            if name_split is None:
                new_name = f'{filename} (1){extension}'
            else:
                name_len = -(len(name_split.group()) + 1)
                name_split_len = -(len(name_split[2]))
                if ' ' == name_file[name_len]:
                    numbers = filename[:name_split_len - 3]
                else:
                    numbers = filename[:name_split_len - 2]
                new_name = f'{numbers} ({int(name_split[2])+1}){extension}'
            name_file = new_name
        return name_file

# проверка имени файла на добавление в список перемещения
    def check(self, mp, names):
        for name in names:
            list_move_to_path = os.listdir(mp)
            if name in list_move_to_path or name in list_files2:
                name_new = self.rename_copy(name, list_move_to_path)
                a, b = f'{path}/{name}', f'{mp}/{name_new}'
                list_files.append((a, b))
                list_files2.append(name_new)
            else:
                a, b = f'{path}/{name}', f'{mp}/{name}'
                list_files.append((a, b))
                list_files2.append(name)

class myApp(QtWidgets.QMainWindow, sort.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(290, 430)

        self.loading()

        self.pushButton_path.clicked.connect(self.browse_folder)
        self.pushButton_choosedirfolders.clicked.connect(self.browse_path_category)

        self.lineEdit_path.setText(path)

        self.pushButton_add_extensions.clicked.connect(self.adds)
        self.pushButton_remove_extensions.clicked.connect(self.remove)
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_removeFolders.clicked.connect(self.removefolders)
        self.pushButton_addFolders.clicked.connect(self.addfolders)
        self.pushButton_settings.clicked.connect(self.settings_win)
        self.listWidget_categori.itemSelectionChanged.connect(self.currCat)
        self.listWidget_categori.setCurrentRow(0)

        self.lineEdit_path.editingFinished.connect(self.replace_path)
        self.lineEdit_pathfolders.editingFinished.connect(self.replace_folders)
        # self.lineEdit_extensions.editingFinished.connect(self.adds_string)
        self.lineEdit_extensions.returnPressed.connect(self.adds_string)
        self.comboBox_lang.activated.connect(self.lang)
        self.comboBox_lang.setCurrentText(saved_lang)
        if self.label_2.text() == '':
            self.lang()

        self.MyThread = MyThread()
        self.MyThread.progress.connect(self.progress)
        self.MyThread.info_not_files.connect(self.info_not_found_files)
        self.MyThread.buttons_stop_text.connect(self.buttons_stop_text)
        self.progressBar.hide()

        QtWidgets.QAction("Quit", self).triggered.connect(self.close)
        self.MyThread.finished.connect(self.finished)

        self.listWidget_categori.doubleClicked.connect(self.edit_category)
        self.listWidget_categori.itemChanged.connect(self.update_rename_cat)

    def buttons_stop_text(self):
        self.pushButton_start.setText(stop_text)

    def info_not_found_files(self):
        self.statusBar.showMessage(status8, 3000)

    def edit_category(self):
        a = self.listWidget_categori.currentItem()
        a.setFlags(a.flags() | QtCore.Qt.ItemIsEditable)
        self.listWidget_categori.editItem(a)

    def replace_keys(self, items):
        dict_all[items[0]] = dict_all.pop(items[1])

    def update_rename_cat(self):
        a = self.listWidget_categori.currentItem().text()

        list_two_cat = []
        if a not in dict_all.keys():
            for i1, k1 in enumerate(dict_all.keys()):
                    for i, k in enumerate(range(self.listWidget_categori.count())):
                        if i1 - 1 == i:
                            list_two_cat.append((self.listWidget_categori.item(i).text(), k1))
            list(map(self.replace_keys, list_two_cat))


    def finished(self, info):
        box = QMessageBox()
        box.setTextFormat(2)
        box.setLayoutDirection(0)
        box.setIcon(QMessageBox.NoIcon)
        box.setWindowIcon(QIcon('move_file.ico'))
        box.setWindowTitle(status7)
        box.setText(info)
        box.setStandardButtons(QMessageBox.Ok)
        self.pushButton_start.setText(start_text)
        box.exec_()
        self.progressBar.hide()



    def closeEvent(self, event):
        # box = QMessageBox()
        # box.setIcon(QMessageBox.Question)
        # box.setWindowIcon(QIcon('move_file.ico'))
        # box.setWindowTitle('Выход?')
        # box.setText('Действительно выйти?')
        # box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # buttonY = box.button(QMessageBox.Yes)
        # buttonY.setText('Да')
        # buttonN = box.button(QMessageBox.No)
        # buttonN.setText('Нет')
        # box.exec_()

        # if box.clickedButton() == buttonY:
        self.write_all()
            # event.accept()
        # elif box.clickedButton() == buttonN:
        #     event.ignore()

    def progress(self, procent):
        self.progressBar.show()
        self.progressBar.setValue(procent)

    def loading(self):
        global saved_lang, path, dict_all, lang
        files = os.listdir(f'{os.path.abspath(os.curdir)}/settings')

        with open('settings/dict_all.json', 'r', encoding="utf-8") as f:
            dict_all = json.load(f)

        with open('settings/lang.json', 'r', encoding="utf-8") as f:
            lang = json.load(f)

        for key in dict_all.keys():
            if key != 'Global_path':
                self.listWidget_categori.addItem(key)

        for key in lang.keys():
            if key != 'Lang':
                self.comboBox_lang.addItem(key)

        g_path = dict_all.get('Global_path')
        path = g_path.get('path')

        d_lang = lang.get('Lang')
        saved_lang = d_lang.get('Cur_lang')

    def lang(self):
        global lang_info, status1, status2, status3, status4, status5, status6, status7, status8, choose_folder, minutes_text, seconds_text, files_count, time_text, size_text, stop_text, start_text, message_stop, status9, status10
        index = self.comboBox_lang.currentText()
        d_lang = lang.get('Lang')
        sl = lang.get(index)
        self.pushButton_path.setText(sl.get('put'))
        self.pushButton_choosedirfolders.setText(sl.get('put'))
        self.label_2.setText(sl.get('trash'))
        self.label_3.setText(sl.get('cur_folder'))
        self.label_4.setText(sl.get('rashirenia'))
        self.label_5.setText(sl.get('category'))
        self.label_8.setText(sl.get('label_enter'))
        self.label_7.setText(sl.get('label_categoria'))
        self.label_lang.setText(sl.get('label_lang'))
        self.label_6.setText(sl.get('label_rashiren'))
        self.pushButton_start.setText(sl.get('start'))

        message_stop = sl.get('message_stop')
        start_text = sl.get('start')
        stop_text = sl.get('stop')
        status1 = sl.get('status1')
        status2 = sl.get('status2')
        status3 = sl.get('status3')
        status4 = sl.get('status4')
        status5 = sl.get('status5')
        choose_folder = sl.get('choose_folder')
        status6 = sl.get('status6')
        status7 = sl.get('status7')
        status8 = sl.get('status8')
        minutes_text = sl.get('minutes_text')
        seconds_text = sl.get('seconds_text')
        files_count = sl.get('files_count')
        time_text = sl.get('time_text')
        size_text = sl.get('size_text')
        status9 = sl.get('status9')
        status10 = sl.get('status10')

        lang_info = sl.get('info')
        if win_size == 0:
            self.pushButton_settings.setText(f'{lang_info} >')
        elif win_size == 1:
            self.pushButton_settings.setText(f'{lang_info} <')

        self.info(index)
        if index != d_lang.get('Cur_lang'):
            lang.update({'Lang': {'Cur_lang': index}})

# добавление файлов по Enter
    def adds_string(self):
        a = self.lineEdit_extensions.text()
        if a.startswith('.'):
            self.adds()
        else:
            self.addfolders()

# замена слешей для винды в строке пути главной папки
    def replace_path(self):
        global path
        a = self.lineEdit_path.text()
        if path != a:
            if os.path.exists(a):
                b = a.replace("\\", "/")
                self.lineEdit_path.setText(b)
                dict_all.update({'Global_path': {'path': b}})
                path = b
            else:
                self.lineEdit_path.setText(path)
                self.statusBar.showMessage(status10, 3000)

# замена слешей для винды в строке пути подпапок
    def replace_folders(self):
        keys = self.cc()
        a = self.lineEdit_pathfolders.text()
        if keys.get('put') != a:
            if os.path.exists(a):
                b = a.replace("\\", "/")
                self.lineEdit_pathfolders.setText(b)
                keys.update({'put': b})
            else:
                self.lineEdit_pathfolders.setText(keys.get('put'))
                self.statusBar.showMessage(status10, 3000)

# отображение и скрытие окна инструкции
    def settings_win(self):
        global win_size
        if win_size == 0:
            self.setFixedSize(590, 430)
            self.pushButton_settings.setText(f'{lang_info} <')
            win_size = 1
            # self.info()
        elif win_size == 1:
            self.setFixedSize(290, 430)
            self.pushButton_settings.setText(f'{lang_info} >')
            win_size = 0

# запись изменений в настройки (расширения/категории/пути/язык)
    def write_all(self):
        with open('settings/dict_all.json', 'w', encoding="utf-8") as f:
            json.dump(dict_all, f, ensure_ascii=False)

        with open('settings/lang.json', 'w', encoding="utf-8") as f:
            json.dump(lang, f, ensure_ascii=False)

# чтение инструкции с диска
    def info(self, readme_lang):
        with open(f'settings/readme_{readme_lang}.ini', 'r') as f:
            a = f.read()
            self.textBrowser.setText(a)

# функция для текущей категории
    def cc(self):
        cur_category = self.listWidget_categori.currentItem().text()
        keys = dict_all.get(cur_category)
        return keys

# отображение всех данный выбранной категории (путь/расширения)
    def currCat(self):
        self.listWidget_extensions.clear()
        self.lineEdit_pathfolders.clear()

        keys = self.cc()
        for i in keys.get('rash'):
            self.listWidget_extensions.addItem(i)
        self.lineEdit_pathfolders.setText(keys.get('put'))
        self.listWidget_extensions.sortItems()

# добавление категорий
    def addfolders(self):
        a = self.lineEdit_extensions.text()
        if a == '':
            self.statusBar.showMessage(status1, 3500)
        else:
            if a in dict_all.keys():
                self.statusBar.showMessage(f'"{a}" - {status9}', 3000)
            else:
                self.listWidget_categori.addItem(a)
                dict_all.update({a: {'put': '', 'rash': []}})
                b = self.listWidget_categori.count()
                self.listWidget_categori.setCurrentRow(b - 1)
        self.lineEdit_extensions.clear()

# удаление категории
    def removefolders(self):
        currItem = self.listWidget_categori.currentItem()
        if not currItem:
            self.statusBar.showMessage(status2, 3000)
        else:
            del dict_all[currItem.text()]
            self.listWidget_categori.takeItem(self.listWidget_categori.row(currItem))

# добавление расширений пачкой или по одному
    def adds(self):
        a = self.lineEdit_extensions.text().lower().split()
        list_ex = []
        if len(a) == 0:
            self.statusBar.showMessage(status3, 3000)
        else:
            keys = self.cc()
            list_rash = keys.get('rash')
            if a[0].startswith('.'):
                for single_a in a:
                    if single_a in list_rash:
                        list_ex.append(single_a)
                    else:
                        list_rash.append(single_a)
                        self.listWidget_extensions.addItem(single_a)
        if len(list_ex) > 0:
            str1 = ' '.join(list_ex)
            self.statusBar.showMessage(f'"{str1}" - {status4}', 3000)
        self.listWidget_extensions.sortItems()
        self.lineEdit_extensions.clear()

# удаление расширений
    def remove(self):
        currItem = self.listWidget_extensions.currentItem()
        if not currItem:
            self.statusBar.showMessage(status5, 3000)
        else:
            keys = self.cc()
            list_rash = keys.get('rash')
            list_rash.remove(currItem.text())
            self.listWidget_extensions.takeItem(self.listWidget_extensions.row(currItem))

# выбор пути для целевой папки
    def browse_folder(self):
        global path
        if path == '' or path.isspace():
            path = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, os.path.expanduser('~'))
        else:
            p = os.path.split(path)[0]
            path = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, os.path.expanduser(p))
        self.lineEdit_path.setText(path)
        dict_all.update({'Global_path': {'path': path}})

#  выбор путей для категорий
    def browse_path_category(self):
        if not self.listWidget_categori.currentItem():
            self.statusBar.showMessage(status6, 3000)
        else:
            if self.lineEdit_pathfolders.text() == '' or self.lineEdit_pathfolders.text().isspace():
                path_choose = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, os.path.expanduser('~'))
            else:
                p = os.path.split(self.lineEdit_pathfolders.text())[0]
                path_choose = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, p)
            keys = self.cc()
            self.lineEdit_pathfolders.setText(path_choose)
            keys.update({'put': path_choose})

# запуск перемещения в отдельном процессе
    def start(self):
        global breaking, starting
        if starting == False:
            self.MyThread.start(5)
            starting = True
        elif starting == True:
            starting = False
            breaking = True
            self.pushButton_start.setText(start_text)
            self.statusBar.showMessage(message_stop, 3000)


def main():
    app = QtWidgets.QApplication(argv)  # Новый экземпляр QApplication
    app.setStyle("Fusion")

    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.Disabled, QPalette.Shadow,
                          QColor(12, 15, 16))

    app.setPalette(dark_palette)

    app.setStyleSheet(
        "QToolTip { color: #ffffff; background-color: #535353; border: 1px groove #333333; }"
        "QTextBrowser { background-color: #353535; border: none; }"
    )

    window = myApp()  # Создаём объект класса myApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()  # то запускаем функцию main()
