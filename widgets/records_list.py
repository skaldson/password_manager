from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class RecordsList(QWidget):

    signal_delete_item = pyqtSignal(str)
    signal_press_item = pyqtSignal(str)
    signal_init_user_info = pyqtSignal()

    def __init__(self, parent=None):
        super(RecordsList, self).__init__(parent)

        self.textQVBoxLayout = QVBoxLayout()
        self.widget_label = QLabel()
        self.textQVBoxLayout.addWidget(self.widget_label)
        self.textQVBoxLayout.setGeometry(QRect(100, 200, 200, 200))
        self.setLayout(self.textQVBoxLayout)  

    @property
    def item_name(self):
        return self.widget_label.text()

    def mouseReleaseEvent(self, event):
        self.x_pos, self.y_pos = event.x(), event.y()

        if event.button() == Qt.LeftButton:
            self.signal_init_user_info.emit()
            self.signal_press_item.emit(self.item_name)
        elif event.button() == Qt.RightButton:
            self.contextMenuEvent(event)

    def contextMenuEvent(self, event):
        widget_menu = QMenu()
        delete_action = widget_menu.addAction('Delete Record')
        action = widget_menu.exec_(self.mapToGlobal(event.pos()))

        login_name = self.item_name

        if action == delete_action:
            self.signal_delete_item.emit(login_name)
