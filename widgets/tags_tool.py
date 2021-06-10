from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from db_files.db_cursor import DBCursor


class TagsTool(QWidget):
    doubleclick_item_signal = pyqtSignal(str)

    def __init__(self, name, parent=None):
        super(TagsTool, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.widget_label = QLabel()
        self.textQVBoxLayout.addWidget(self.widget_label)
        self.textQVBoxLayout.setGeometry(QRect(100, 50, 50, 50))
        self.setLayout(self.textQVBoxLayout)

        self.name = name

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.doubleclick_item_signal.emit(self.name)
