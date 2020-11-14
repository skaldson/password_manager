from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import window_ui_py.edit_section_py as edit_section
from db_files.db_cursor import DBCursor


class EditSection(QWidget, edit_section.Ui_Form):
    def __init__(self, parent=None):
        super(EditSection, self).__init__()
        self.setupUi(self)
