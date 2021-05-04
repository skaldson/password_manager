from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import window_ui_py.new_name_window_py as new_name
from message_boxes import InfoBox
from db_files.db_cursor import DBCursor
from record_abs_class import is_unique_name, user_records


class NewName(QDialog, new_name.Ui_new_name_window):
    new_name_signal = pyqtSignal(str)
    
    def __init__(self):
        super(NewName, self).__init__()
        self.setupUi(self)

    def init_functionality(self):
        self.submit_button.clicked.connect(self.submit_new_name)
        self.setModal(True)
        self.exec_()

    def submit_new_name(self):
        records_list = user_records()
        record_name = self.new_name.text()
        if record_name:
            if len(record_name) < 4:
                message = 'Record name must contain at least 4 letters'
                InfoBox(self, message)
            else:
                unique_name = is_unique_name(records_list, record_name, self)
                if unique_name:
                    self.new_name_signal.emit(record_name)
                    self.close()
                else:
                    pass
