from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor, QPalette
import sys
import sort
import shutil
import os
import pickle

win_size = 0
path = ''
dict_all = {}


class myApp(QtWidgets.QMainWindow, sort.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(290, 410)
        self.setupUi(self)

        self.loading()

        self.pushButton_path.clicked.connect(self.browse_folder)
        self.pushButton_choosedirfolders.clicked.connect(self.qwerty)

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

        # self.comboBox_lang.setCurrentIndex(current_lang)
        self.comboBox_lang.activated.connect(self.lang)
        self.comboBox_lang.setCurrentIndex(current_lang)
        if self.label_2.text() == '':
            self.lang()

    def loading(self):
        files = os.listdir(f'{os.path.abspath(os.curdir)}/settings')
        if not 'dict_all.ini' in files:  # проверка на существование файла в папке
            with open('settings/dict_all.ini', 'wb') as f:
                global dict_all
                dict_all.clear()
                pickle.dump(dict_all, f)

        if not 'path.ini' in files:  # проверка на существование файла в папке
            with open('settings/path.ini', 'wb') as f:
                global path
                pickle.dump(path, f)

        try:
            with open('settings/dict_all.ini', 'rb') as f:
                dict_all = pickle.load(f)

            with open('settings/path.ini', 'rb') as f:
                path = pickle.load(f)

            with open('settings/lang.ini', 'rb') as f:
                global lang
                lang = pickle.load(f)

            with open('settings/current_lang.ini', 'rb') as f:
                global current_lang
                current_lang = pickle.load(f)

            for value in dict_all.keys():
                self.listWidget_categori.addItem(value)

            for key in lang.keys():
                self.comboBox_lang.addItem(key)
        except:
            pass

    def lang(self):
        index = self.comboBox_lang.currentIndex()
        # if index != current_lang:
        for i, (k, v) in enumerate(lang.items()):
            if i == index:
                for k2, v2 in v.items():
                    if k2 == 'put':
                        self.pushButton_path.setText(v2)
                        self.pushButton_choosedirfolders.setText(v2)
                    elif k2 == 'trash':
                        self.label_2.setText(v2)
                    elif k2 == 'cur_folder':
                        self.label_3.setText(v2)
                    elif k2 == 'category':
                        self.label_5.setText(v2)
                    elif k2 == 'rashirenia':
                        self.label_4.setText(v2)
                    elif k2 == 'label_enter':
                        self.label_8.setText(v2)
                    elif k2 == 'label_categoria':
                        self.label_7.setText(v2)
                    elif k2 == 'label_lang':
                        self.label_lang.setText(v2)
                    elif k2 == 'label_rashiren':
                        self.label_6.setText(v2)
                    elif k2 == 'start':
                        self.pushButton_start.setText(v2)
                    elif k2 == 'info':
                        global lang_info
                        lang_info = v2
                        if win_size == 0:
                            self.pushButton_settings.setText(f'{v2} >')
                        elif win_size == 1:
                            self.pushButton_settings.setText(f'{v2} <')
                    elif k2 == 'status1':
                        global status1
                        status1 = v2
                    elif k2 == 'status2':
                        global status2
                        status2 = v2
                    elif k2 == 'status3':
                        global status3
                        status3 = v2
                    elif k2 == 'status4':
                        global status4
                        status4 = v2
                    elif k2 == 'status5':
                        global status5
                        status5 = v2
                    elif k2 == 'choose_folder':
                        global choose_folder
                        choose_folder = v2
                    elif k2 == 'status6':
                        global status6
                        status6 = v2
                    elif k2 == 'status7':
                        global status7
                        status7 = v2
                global current_lang
                current_lang = index
                self.w_lang()

                if win_size == 1:
                    self.info()

    def adds_string(self):
        a = self.lineEdit_extensions.text()
        if a.startswith('.'):
            self.adds()
        else:
            self.addfolders()

# замена слешей для винды в строке пути главной папки
    def replace_path(self):
        global path
        if path != self.lineEdit_path.text():
            a = self.lineEdit_path.text()
            aa = os.path.normpath(a)
            b = aa.replace("\\", "/")
            self.lineEdit_path.setText(b)
            path = b
            self.w_path()

# замена слешей для винды в строке пути подпапок
    def replace_folders(self):
        index_categori = self.listWidget_categori.currentRow()
        a = self.lineEdit_pathfolders.text()
        for i, (k, v) in enumerate(dict_all.items()):
            if i == index_categori:
                for p, v2 in v.items():
                    if p == 'put' and a != v2:
                        aa = os.path.normpath(a)
                        b = aa.replace("\\", "/")
                        self.lineEdit_pathfolders.setText(b)
                        v.update({p: b})
                        self.write_all()

    def settings_win(self):
        # self.info()
        global win_size
        if win_size == 0:
            self.setFixedSize(590, 410)
            self.pushButton_settings.setText(f'{lang_info} <')
            win_size = 1
            self.info()
        elif win_size == 1:
            self.setFixedSize(290, 410)
            self.pushButton_settings.setText(f'{lang_info} >')
            win_size = 0

    def ww_lang(self):
        with open('settings/lang.ini', 'wb') as f:
            pickle.dump(lang, f)

    def w_lang(self):
        with open('settings/current_lang.ini', 'wb') as f:
            pickle.dump(current_lang, f)

    def w_path(self):
        with open('settings/path.ini', 'wb') as f:
            pickle.dump(path, f)

    def write_all(self):
        with open('settings/dict_all.ini', 'wb') as f:
            pickle.dump(dict_all, f)

    def info(self):
        if current_lang == 0:
            with open('settings/readme_ru.ini', 'r') as f:
                a = f.read()
                self.textBrowser.setText(a)
                f.close()
        elif current_lang == 1:
            with open('settings/readme_en.ini', 'r') as f:
                a = f.read()
                self.textBrowser.setText(a)
                f.close()

    def currCat(self):
        index_categori = self.listWidget_categori.currentRow()
        self.listWidget_extensions.clear()
        self.lineEdit_pathfolders.clear()

        for i, (k, v) in enumerate(dict_all.items()):
            if i == index_categori:
                for key, value in v.items():
                    if key == 'rash':
                        for i2 in value:
                            self.listWidget_extensions.addItem(i2)
                    else:
                        self.lineEdit_pathfolders.setText(value)
        self.listWidget_extensions.sortItems()

    def addfolders(self):
        a = self.lineEdit_extensions.text()
        if a == '':
            self.statusBar.showMessage(status1, 3500)
        else:
            text_line = self.lineEdit_extensions.text()
            self.listWidget_categori.addItem(text_line)
            dict_all.update({text_line: {'put': '', 'rash': []}})
            self.lineEdit_extensions.clear()
            b = self.listWidget_categori.count()
            self.listWidget_categori.setCurrentRow(b - 1)
            self.write_all()

    def removefolders(self):
        currItem = self.listWidget_categori.currentItem()
        if not currItem:
            self.statusBar.showMessage(status2, 3000)
        else:
            index_category = self.listWidget_categori.currentRow()
            for index, (key, value) in enumerate(list(dict_all.items())):
                if index_category == index:
                    del dict_all[key]
                    self.listWidget_categori.takeItem(self.listWidget_categori.row(currItem))
            self.write_all()

    def adds(self):
        a = self.lineEdit_extensions.text().lower()
        if a == '':
            self.statusBar.showMessage(status3, 3000)
        else:
            index_category = self.listWidget_categori.currentRow()
            # перебор индексов, ключей и русских названий
            for i, (k, v) in enumerate(dict_all.items()):
                if i == index_category:
                    for key, value in v.items():
                        if key == 'rash' and a.startswith('.'):
                            b = a.split()
                            for i2 in b:
                                if i2 in value:
                                    self.statusBar.showMessage(status4, 3000)
                                else:
                                    value.append(i2)
                                    self.listWidget_extensions.addItem(i2)
        self.listWidget_extensions.sortItems()
        self.lineEdit_extensions.clear()
        self.write_all()

    def remove(self):
        currItemNot = self.listWidget_extensions.currentItem()
        if not currItemNot:
            self.statusBar.showMessage(status5, 3000)
        else:
            currItem = self.listWidget_extensions.currentItem().text()
            currItem2 = self.listWidget_extensions.currentItem()

            index_category = self.listWidget_categori.currentRow()
            # перебор индексов, ключей и русских названий
            for i, (k, v) in enumerate(dict_all.items()):
                if i == index_category:
                    for key, value in v.items():
                        if key == 'rash':
                            value.remove(currItem)
                            self.listWidget_extensions.takeItem(self.listWidget_extensions.row(currItem2))
            self.write_all()

    def browse_folder(self):  # выбор дирректории
        global path
        path = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, os.path.expanduser('~'))
        os.path.normpath(path)
        self.lineEdit_path.setText(path)
        self.w_path()

    def qwerty(self):
        index_category = self.listWidget_categori.currentRow()
        if index_category == -1:
            self.statusBar.showMessage(status6, 3000)
        else:
            for i, (k, v) in enumerate(dict_all.items()):
                if index_category == i:
                    for k2, v2 in v.items():
                        if k2 == 'put':
                            path_choose = QtWidgets.QFileDialog.getExistingDirectory(self, choose_folder, os.path.expanduser('~'))
                            os.path.normpath(path_choose)
                            self.lineEdit_pathfolders.setText(path_choose)
                            v.update({k2: path_choose})
            self.write_all()

    def start(self):
        files = os.listdir(path)
        for ind, (knd, v) in enumerate(dict_all.items()):
            for pk, pv in v.items():
                if pk == 'put' and pv != '' and os.path.exists(pv):
                    for rk, rv in v.items():
                        if rk == 'rash':
                            for rashiren in rv:
                                for i in files:
                                    if i.endswith(rashiren):
                                        if i in (os.listdir(pv)):
                                            new_name = f'{i[:-len(rashiren)]}_{rashiren}'
                                            shutil.move(f'{path}/{i}', f'{pv}/{new_name}')
                                        else:
                                            shutil.move(f'{path}/{i}', f'{pv}/{i}')
        self.statusBar.showMessage(status7, 3000)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
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


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
