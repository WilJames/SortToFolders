from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtGui import QColor, QPalette, QIcon
from sys import argv
from shutil import move
from re import search
from time import time, sleep

import GUI
import os
import json

breaking = False
starting = False
win_size = 0
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
        starting = False

    def humansize(self, nbytes):
        '''
        Перевод байт в кб, мб и т.д.
        '''
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        i = 0
        while nbytes >= 1024 and i < len(suffixes)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])

    def parsing_listdir(self):
        '''
        Парсинг файлов в целевой папке
        '''
        files = []
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    files.append(os.fsdecode(entry.name))
        return files

    def parsing_dict(self, category):
        '''
        пасинг словаря для получения пути и расширений для категории
        '''
        dict_cat = dict_all.get(category)
        put = dict_cat.get('put')
        if put != '' and put != path and os.path.exists(put):
            rash = dict_cat.get('rash')
            return put, rash
        else:
            return None, None

    def parsing_rash(self, extensions, files):
        '''
        парсинг расширений и соответсвия им файлам
        '''
        names = []
        for extension in extensions:
            for name in files:
                filename, ext = os.path.splitext(name)
                if ext.lower() == extension:
                    names.append(name)
        return names

    def rename_copy(self, name_file, list_move_to_path):
        '''
        переименование файла если такое имя есть в папке для перемещения
        '''
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

    def check(self, mp, names):
        '''
        проверка имени файла на добавление в список перемещения
        '''
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

class myApp(QtWidgets.QMainWindow, GUI.Ui_MainWindow):
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
        self.lineEdit_path.returnPressed.connect(self.clear_focus_path)

        self.lineEdit_pathfolders.editingFinished.connect(self.replace_folders)
        self.lineEdit_pathfolders.returnPressed.connect(self.clear_focus_pathfolders)

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
        self.statusBar.showMessage(st8, 3000)

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
        box.setWindowTitle(st7)
        box.setText(info)
        box.setStandardButtons(QMessageBox.Ok)
        self.pushButton_start.setText(start_text)
        box.exec_()
        self.progressBar.hide()



    def closeEvent(self, event):
        self.write_all()

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
        global lang_info, st1, st2, st3, st4, st5, st6, st7, st8, choose_folder, minutes_text, seconds_text, files_count, time_text, size_text, stop_text, start_text, message_stop, st9, st10, st11, st12
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
        st1 = sl.get('st1')
        st2 = sl.get('st2')
        st3 = sl.get('st3')
        st4 = sl.get('st4')
        st5 = sl.get('st5')
        choose_folder = sl.get('choose_folder')
        st6 = sl.get('st6')
        st7 = sl.get('st7')
        st8 = sl.get('st8')
        minutes_text = sl.get('minutes_text')
        seconds_text = sl.get('seconds_text')
        files_count = sl.get('files_count')
        time_text = sl.get('time_text')
        size_text = sl.get('size_text')
        st9 = sl.get('st9')
        st10 = sl.get('st10')
        st11 = sl.get('st11')
        st12 = sl.get('st12')

        lang_info = sl.get('info')
        if win_size == 0:
            self.pushButton_settings.setText(f'{lang_info} >')
        elif win_size == 1:
            self.pushButton_settings.setText(f'{lang_info} <')

        self.info(index)
        if index != d_lang.get('Cur_lang'):
            lang.update({'Lang': {'Cur_lang': index}})

    def adds_string(self):
        # добавление файлов по Enter
        a = self.lineEdit_extensions.text()
        if a.startswith('.'):
            self.adds()
        else:
            self.addfolders()

    def replace_path(self):
        # замена слешей для винды в строке пути главной папки
        global path
        a = self.lineEdit_path.text()
        if path != a and a != '':
            if os.path.exists(a):
                b = a.replace("\\", "/")
                self.lineEdit_path.setText(b)
                dict_all.update({'Global_path': {'path': b}})
                path = b
            else:
                self.lineEdit_path.setText(path)
                self.statusBar.showMessage(st10, 3000)
        elif a == '':
            dict_all.update({'Global_path': {'path': a}})
            path = a

    def replace_folders(self):
        # замена слешей для винды в строке пути подпапок
        keys = self.cc()
        a = self.lineEdit_pathfolders.text()
        if keys.get('put') != a and a != '':
            if os.path.exists(a):
                b = a.replace("\\", "/")
                self.lineEdit_pathfolders.setText(b)
                keys.update({'put': b})
            else:
                self.lineEdit_pathfolders.setText(keys.get('put'))
                self.statusBar.showMessage(st10, 3000)
        elif a == '':
            keys.update({'put': ''})

    def clear_focus_path(self):
        self.lineEdit_path.clearFocus()

    def clear_focus_pathfolders(self):
        self.lineEdit_pathfolders.clearFocus()

    def settings_win(self):
        # отображение и скрытие окна инструкции
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

    def write_all(self):
        # запись изменений в настройки (расширения/категории/пути/язык)
        with open('settings/dict_all.json', 'w', encoding="utf-8") as f:
            json.dump(dict_all, f, ensure_ascii=False)

        with open('settings/lang.json', 'w', encoding="utf-8") as f:
            json.dump(lang, f, ensure_ascii=False)

    def info(self, readme_lang):
        # чтение инструкции с диска
        with open(f'settings/readme_{readme_lang}.ini', 'r') as f:
            a = f.read()
            self.textBrowser.setText(a)

    def cc(self):
        # функция для текущей категории
        cur_category = self.listWidget_categori.currentItem().text()
        keys = dict_all.get(cur_category)
        return keys

    def currCat(self):
        # отображение всех данный выбранной категории (путь/расширения)
        self.listWidget_extensions.clear()
        self.lineEdit_pathfolders.clear()

        keys = self.cc()
        for i in keys.get('rash'):
            self.listWidget_extensions.addItem(i)
        self.lineEdit_pathfolders.setText(keys.get('put'))
        self.listWidget_extensions.sortItems()

    def addfolders(self):
        # добавление категорий
        a = self.lineEdit_extensions.text()
        if a == '':
            self.statusBar.showMessage(st1, 3500)
        else:
            if a in dict_all.keys():
                self.statusBar.showMessage(f'"{a}" - {st9}', 3000)
            else:
                self.listWidget_categori.addItem(a)
                dict_all.update({a: {'put': '', 'rash': []}})
                b = self.listWidget_categori.count()
                self.listWidget_categori.setCurrentRow(b - 1)
        self.lineEdit_extensions.clear()

    def removefolders(self):
        # удаление категории
        currItem = self.listWidget_categori.currentItem()
        if not currItem:
            self.statusBar.showMessage(st2, 3000)
        else:
            del dict_all[currItem.text()]
            self.listWidget_categori.takeItem(self.listWidget_categori.row(currItem))


    def adds(self):
        # добавление расширений пачкой или по одному
        a = self.lineEdit_extensions.text().lower().split()
        list_ex = []
        if len(a) == 0:
            self.statusBar.showMessage(st3, 3000)
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
            self.statusBar.showMessage(f'"{str1}" - {st4}', 3000)
        self.listWidget_extensions.sortItems()
        self.lineEdit_extensions.clear()

    def remove(self):
        # удаление расширений
        currItem = self.listWidget_extensions.currentItem()
        if not currItem:
            self.statusBar.showMessage(st5, 3000)
        else:
            keys = self.cc()
            list_rash = keys.get('rash')
            list_rash.remove(currItem.text())
            self.listWidget_extensions.takeItem(self.listWidget_extensions.row(currItem))

    def browse_folder(self):
        # выбор пути для целевой папки
        global path
        if path == '' or path.isspace():
            path = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, os.path.expanduser('~'))
        else:
            p = os.path.split(path)[0]
            path = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, os.path.expanduser(p))
        self.lineEdit_path.setText(path)
        dict_all.update({'Global_path': {'path': path}})

    def browse_path_category(self):
        #  выбор путей для категорий
        if not self.listWidget_categori.currentItem():
            self.statusBar.showMessage(st6, 3000)
        else:
            if self.lineEdit_pathfolders.text() == '' or self.lineEdit_pathfolders.text().isspace():
                path_choose = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, os.path.expanduser('~'))
            else:
                p = os.path.split(self.lineEdit_pathfolders.text())[0]
                path_choose = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, p)
            keys = self.cc()
            self.lineEdit_pathfolders.setText(path_choose)
            keys.update({'put': path_choose})

    def start(self):
        # запуск перемещения в отдельном процессе
        global breaking, starting
        if starting == False:
            if path == '':
                self.statusBar.showMessage(st11, 3000)
            elif not os.path.exists(path):
                self.statusBar.showMessage(st12, 3000)
            else:
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
