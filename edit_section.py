from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from db_files.db_cursor import DBCursor
import window_ui_py.edit_section_py as edit_section



class EditSection(QWidget, edit_section.Ui_Form):

    signal_current_record = pyqtSignal(int)

    def __init__(self, parent=None):
        super(EditSection, self).__init__()
        self.setupUi(self)

        self.scroll_tag_area.setWidget(self.edit_tag_widget)
        self.db_cursor = DBCursor.getInstance()
        self.current_record_id = 0

    def init_record_index(self, record_name):
        self.edit_tag_widget.record_name = record_name

    def init_edit_tag_list(self):
        self.edit_tag_widget.tags_list = self.db_cursor.get_tags_by_login_name(self.edit_tag_widget.record_name)