from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import window_ui_py.new_name_window_py as new_name
from windows.utility.message_boxes import InfoBox
from db_files.db_cursor import DBCursor
from windows.utility.abs_records import is_unique_name, user_records
from windows.correct_input import delete_rspace


class NewName(QDialog, new_name.Ui_new_name_window):
    new_name_signal = pyqtSignal(str)
    
    def __init__(self, custom_name=False):
        super(NewName, self).__init__()
        self.setupUi(self)
        self.custom_name = custom_name

    def modal_window(self):
        self.setModal(True)
        self.exec_()
    
    def init_functionality(self):
        if not self.custom_name:
            self.submit_button.clicked.connect(self.submit_new_login_name)
            self.modal_window()
        else:
            self.submit_button.clicked.connect(self.submit_new_name)
            self.modal_window()
    
    def lt_four_symbol(self):
        temp_name = delete_rspace(self.new_name.text())
        self.new_name.setText(temp_name)
        if len(self.new_name.text()) < 4:
            message = 'Record name must contain at least 4 letters'
            InfoBox(self, message)
            return True
        else:
            return False

    def submit_new_login_name(self):
        records_list = user_records()
        record_name = self.new_name.text()
        if record_name:
            if self.lt_four_symbol():
                pass
            else:
                unique_name = is_unique_name(records_list, record_name, self)
                if unique_name:
                    self.new_name_signal.emit(record_name)
                    self.close()
                else:
                    pass

    def submit_new_name(self):
        record_name = self.new_name.text()
        check_input = self.lt_four_symbol()
        print(check_input)
        if check_input:
            pass
        else:
            self.new_name_signal.emit(record_name)
