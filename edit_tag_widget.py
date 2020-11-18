import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from tags_widget import TagWidget


class EditTagWidget(TagWidget):
    def __init__(self, parent=None):
        super(EditTagWidget, self).__init__()

        # self.db_cursor = DBCursor.getInstance()
        self.record_name = 0
        self.tags_list = 0

# зробити так, щоб помічені теги викидалися наперед у головному TagWidget
    def paintEvent(self, event):
        print(self.tags_list)
