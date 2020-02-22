# -*- coding: utf-8 -*-
from PySide2.QtGui import QPalette, QColor

WHITE = QColor(255, 255, 255)
BLACK = QColor(0, 0, 0)
RED = QColor(255, 0, 0)
PRIMARY = QColor(53, 53, 53)
SECONDARY = QColor(25, 25, 25)
TERTIARY = QColor(42, 130, 218)
DISABLEDSHADOW = QColor(12, 15, 16)
DARKGRAY = QColor(80, 80, 80)
'''
-HighlightedText 42, 130, 218
highlight_text_color = Qt.white HighlightedText
'''

def css_rgb(color, a=False):
    """Get a CSS `rgb` or `rgba` string from a `QtGui.QColor`."""
    return ("rgba({}, {}, {}, {})" if a else "rgb({}, {}, {})").format(*color.getRgb())

class QDarkPalette(QPalette):
    """Dark palette for a Qt application meant to be used with the Fusion theme."""
    def __init__(self, *__args):
        super().__init__(*__args)

        # Set all the colors based on the constants in globals
        self.setColor(QPalette.Window, PRIMARY)
        self.setColor(QPalette.WindowText, WHITE)
        self.setColor(QPalette.Base, SECONDARY)
        self.setColor(QPalette.AlternateBase, PRIMARY)
        self.setColor(QPalette.ToolTipBase, WHITE)
        self.setColor(QPalette.ToolTipText, WHITE)
        self.setColor(QPalette.Text, WHITE)
        self.setColor(QPalette.Button, PRIMARY)
        self.setColor(QPalette.ButtonText, WHITE)
        self.setColor(QPalette.BrightText, RED)
        self.setColor(QPalette.Link, TERTIARY)
        self.setColor(QPalette.Highlight, TERTIARY)
        self.setColor(QPalette.HighlightedText, BLACK)
        self.setColor(QPalette.PlaceholderText, DARKGRAY)
        self.setColor(QPalette.Disabled, QPalette.Light, BLACK) #+
        self.setColor(QPalette.Disabled, QPalette.Shadow, DISABLEDSHADOW) #+
        self.setColor(QPalette.Disabled, QPalette.WindowText, DARKGRAY)
        self.setColor(QPalette.Disabled, QPalette.Text, DARKGRAY)
        self.setColor(QPalette.Disabled, QPalette.ButtonText, DARKGRAY)

    @staticmethod
    def set_stylesheet(app):
        """Static method to set the tooltip stylesheet to a `QtWidgets.QApplication`."""
        app.setStyleSheet("""
                        QToolTip {{ color: {white};
                                    background-color: {tertiary};
                                    border: 1px solid {white}; }}
                        QTextBrowser {{ background-color: #353535;
                                        border: none; }}
                        QLineEdit {{ border: none;
                                    border-radius: 1px;
                                    background: {secondary};
                                    selection-background-color: {tertiary};}}
                        """.format(white=css_rgb(WHITE), tertiary=css_rgb(TERTIARY), primary=css_rgb(PRIMARY), secondary=css_rgb(SECONDARY)))

    def set_app(self, app):
        """Set the Fusion theme and this palette to a `QtWidgets.QApplication`."""
        app.setStyle("Fusion")
        app.setPalette(self)
        self.set_stylesheet(app)
