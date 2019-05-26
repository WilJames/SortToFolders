from PyQt5 import QtWidgets, QtCore
from transliterate import translit, get_available_language_codes
from PyQt5.QtGui import QColor, QPalette
import sys
import sort
import shutil
import os
import pickle

win_size = 0
path = ''

with open('settings/path.ini', 'rb') as f:
    path = pickle.load(f)

with open('settings/dict_all_paths.ini', 'rb') as f:
    dict_all_paths = pickle.load(f)
with open('settings/dict_folders.ini', 'rb') as f:
    dict_folders = pickle.load(f)
with open('settings/dict_extensions.ini', 'rb') as f:
    dict_extensions = pickle.load(f)

# dict_all_paths = {
#     'archves': 'C:/dev',
#     'video': 'C:/dev',
#     'documents': 'C:/dev',
#     'images': 'C:/dev',
#     'music': 'C:/dev',
#     'programs': 'C:/dev',
#     'obrazu': 'C:/dev',
#     'psd': 'C:/dev',
#     'fonts': 'C:/dev',
#     'torrent': 'C:/dev'
# }

# dict_folders = {
#     'archves': 'Архивы',
#     'video': 'Видео',
#     'documents': 'Документы',
#     'images': 'Изображения',
#     'music': 'Музыка',
#     'programs': 'Программы',
#     'obrazu': 'Образы',
#     'psd': 'CG редакторы',
#     'fonts': 'Шрифты',
#     'torrent': 'Торренты'
# }

# dict_extensions = {
#     'archves': ['.zip', '.rar', '.arj', '.gz', '.sit', '.sitx', '.sea', '.ace', '.bz2', '.7z', '.jar', '.cab'],
#     'video': ['.avi', '.mpg', '.mpe', '.mpeg', '.asf', '.wmv', '.mov', '.qt', '.rm', '.mp4', '.flv', '.m4v', '.webm', '.ogv', '.ogg', '.mkv', '.3gp', '.3gpp', '.bik', '.flv'],
#     'documents': ['.doc', '.pdf', '.ppt', '.pps', '.docx', '.pptx', '.txt'],
#     'images': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.jpe', '.jfif', '.tigg'],
#     'music': ['.mp3', '.wav', '.wma', '.mpa', '.ram', '.ra', '.aac', '.aif', '.m4a'],
#     'programs': ['.exe', '.msi'],
#     'obrazu': ['.iso', '.mdf', '.mds'],
#     'psd': ['.psd'],
#     'fonts': ['.ttf'],
#     'torrent': ['.torrent']
# }


# class mySet(QtWidgets.QWidget, sort2.Ui_settings):
#     def __init__(self):
#         super().__init__()
#         self.setFixedSize(371, 340)
#         self.setupUi(self)


class myApp(QtWidgets.QMainWindow, sort.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(290, 410)
        self.setupUi(self)

        self.pushButton_path.clicked.connect(self.browse_folder)
        self.pushButton_choosedirfolders.clicked.connect(self.qwerty)

        self.lineEdit_path.setText(path)
        self.info()

        for value in dict_folders.values():
            self.listWidget_categori.addItem(value)

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

    def adds_string(self):
        a = self.lineEdit_extensions.text()
        if a.startswith('.'):
            self.adds()
        else:
            self.addfolders()

    def replace_path(self):
        global path
        if path != self.lineEdit_path.text():
            a = self.lineEdit_path.text()
            b = a.replace("\\", "/")
            self.lineEdit_path.setText(b)
            path = b
            self.w_path()

    def replace_folders(self):
        index_categori = self.listWidget_categori.currentRow()
        a = self.lineEdit_pathfolders.text()
        for index_p, (key_p, value_p) in enumerate(dict_all_paths.items()):
            if index_categori == index_p:
                if a != value_p:
                    b = a.replace("\\", "/")
                    self.lineEdit_pathfolders.setText(b)
                    dict_all_paths.update({key_p: b})
                    self.w_dict_all_paths()

    def settings_win(self):
        # self.statusBar.showMessage('Message in statusbar.', 2000)
        global win_size
        if win_size == 0:
            self.setFixedSize(590, 410)
            self.pushButton_settings.setText('Инструкция <')
            win_size = 1
        elif win_size == 1:
            self.setFixedSize(290, 410)
            self.pushButton_settings.setText('Инструкция >')
            win_size = 0

    def w_path(self):
        files = os.listdir(f'{os.path.abspath(os.curdir)}/settings')
        if 'path.ini' in files:  # проверка на существование файла в папке
            with open('settings/path.ini', 'wb') as f:
                pickle.dump(path, f)
        else:
            create_file = open('settings/path.ini', 'w')  # создание файла
            create_file.close()
            with open('settings/path.ini', 'wb') as f:
                pickle.dump(path, f)

    def w_dict_folders(self):
        files = os.listdir(f'{os.path.abspath(os.curdir)}/settings')
        if 'dict_folders.ini' in files:  # проверка на существование файла в папке
            with open('settings/dict_folders.ini', 'wb') as f:
                pickle.dump(dict_folders, f)
        else:
            create_file = open('settings/dict_folders.ini',
                               'w')  # создание файла
            create_file.close()
            with open('settings/dict_folders.ini', 'wb') as f:
                pickle.dump(dict_folders, f)

    def w_dict_extensions(self):
        files = os.listdir(f'{os.path.abspath(os.curdir)}/settings')
        if 'dict_extensions.ini' in files:  # проверка на существование файла в папке
            with open('settings/dict_extensions.ini', 'wb') as f:
                pickle.dump(dict_extensions, f)
        else:
            create_file = open('settings/dict_extensions.ini',
                               'w')  # создание файла
            create_file.close()
            with open('settings/dict_extensions.ini', 'wb') as f:
                pickle.dump(dict_extensions, f)

    def w_dict_all_paths(self):
        files = os.listdir(f'{os.path.abspath(os.curdir)}/settings')
        if 'dict_all_paths.ini' in files:  # проверка на существование файла в папке
            with open('settings/dict_all_paths.ini', 'wb') as f:
                pickle.dump(dict_all_paths, f)
        else:
            create_file = open('settings/dict_all_paths.ini',
                               'w')  # создание файла
            create_file.close()
            with open('settings/dict_all_paths.ini', 'wb') as f:
                pickle.dump(dict_all_paths, f)

    def info(self):
        with open('settings/readme.ini', 'r') as f:
            a = f.read()
            self.textBrowser.setText(a)
            f.close()

    def currCat(self):
        index_categori = self.listWidget_categori.currentRow()
        self.listWidget_extensions.clear()
        self.lineEdit_pathfolders.clear()

        for index, (key, value) in enumerate(dict_extensions.items()):
            for index_p, (key_p, value_p) in enumerate(dict_all_paths.items()):
                if index_categori == index == index_p:
                    self.lineEdit_pathfolders.setText(value_p)
                    for k in value:
                        self.listWidget_extensions.addItem(k)
        self.listWidget_extensions.sortItems()

    def addfolders(self):
        a = self.lineEdit_extensions.text()
        if a == '':
            self.statusBar.showMessage('Введите название категории для добавления!', 3500)
        else:
            text_line = self.lineEdit_extensions.text()
            self.listWidget_categori.addItem(text_line)
            text_line_translit = translit(text_line, 'ru', reversed=True)
            dict_folders.update({text_line_translit: text_line})
            dict_extensions.update({text_line_translit: []})
            dict_all_paths.update({text_line_translit: ''})
            self.lineEdit_extensions.clear()
            self.w_dict_folders()
            self.w_dict_extensions()
            self.w_dict_all_paths()
            b = self.listWidget_categori.count()
            self.listWidget_categori.setCurrentRow(b - 1)
            # self.currCat()

    def removefolders(self):
        currItemNot = self.listWidget_categori.currentItem()
        if not currItemNot:
            self.statusBar.showMessage('Не выбрана категория для удаления!', 3000)
        else:
            currItem = self.listWidget_categori.currentItem()
            index_category = self.listWidget_categori.currentRow()
            for index, (key, value) in enumerate(list(dict_folders.items())):
                if index_category == index:
                    del dict_folders[key]
                    del dict_extensions[key]
                    del dict_all_paths[key]
                    # self.comboBox_folders.removeItem(index_category)
                    self.listWidget_categori.takeItem(self.listWidget_categori.row(currItem))

            # self.currCat()
            self.w_dict_folders()
            self.w_dict_extensions()
            self.w_dict_all_paths()

    def adds(self):
        a = self.lineEdit_extensions.text()
        if a == '':
            self.statusBar.showMessage('Введите расширение для добавления!', 3000)
        else:
            index_category = self.listWidget_categori.currentRow()
            # перебор индексов, ключей и русских названий
            for index, (key, value) in enumerate(dict_folders.items()):
                if index_category == index:  # проверка индекса категории и русских имен категорий
                    for index_ras, (key_ras, value_ras) in enumerate(
                            dict_extensions.items()):
                        if key_ras == key:
                            if a.startswith('.'):
                                b = a.split()
                                for i in b:
                                    value_ras.append(i)
                                    dict_extensions.update({key_ras: value_ras})
                                    self.listWidget_extensions.addItem(i)
            self.listWidget_extensions.sortItems()
            self.lineEdit_extensions.clear()
            self.w_dict_extensions()

    def remove(self):
        currItemNot = self.listWidget_extensions.currentItem()
        if not currItemNot:
            self.statusBar.showMessage('Не выбрано расширение для удаления!', 3000)
        else:
            currItem = self.listWidget_extensions.currentItem().text()
            currItem2 = self.listWidget_extensions.currentItem()

            index_category = self.listWidget_categori.currentRow()
            # перебор индексов, ключей и русских названий
            for index, (key, value) in enumerate(dict_folders.items()):
                if index_category == index:  # проверка индекса категории и русских имен категорий
                    for index_ras, (key_ras, value_ras) in enumerate(dict_extensions.items()):
                        if key_ras == key:
                            value_ras.remove(currItem)
                            dict_extensions.update({key_ras: value_ras})
                            self.listWidget_extensions.takeItem(self.listWidget_extensions.row(currItem2))
            self.w_dict_extensions()

    def browse_folder(self):  # выбор дирректории
        global path
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Выберите папку")
        self.lineEdit_path.setText(path)
        self.w_path()

    def qwerty(self):
        index_category = self.listWidget_categori.currentRow()
        if index_category == -1:
            self.statusBar.showMessage('Выберите категорию!', 3000)
        else:
            for index, (key, value) in enumerate(dict_all_paths.items()):
                if index_category == index:
                    path_choose = QtWidgets.QFileDialog.getExistingDirectory(
                        self, "Выберите папку")
                    self.lineEdit_pathfolders.setText(path_choose)
                    dict_all_paths.update({key: path_choose})
                    self.w_dict_all_paths()

    def start(self):
        files = os.listdir(path)
        for index_p, (key_p, value_p) in enumerate(dict_all_paths.items()):
            for index_r, (key_r,
                          value_r) in enumerate(dict_extensions.items()):
                if index_p == index_r and value_p != '':
                    for rashiren in value_r:
                        for i in files:
                            if i.endswith(rashiren):
                                if i in (os.listdir(value_p)):
                                    k = f'{i[:-len(rashiren)]}_{rashiren}'
                                    shutil.move(f'{path}/{i}',
                                                f'{value_p}/{k}')
                                else:
                                    shutil.move(f'{path}/{i}',
                                                f'{value_p}/{i}')
        self.statusBar.showMessage('Завершено!', 3000)


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
        "QTextBrowser { background-color: #333333; border: none; }"
    )

    window = myApp()  # Создаём объект класса myApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
