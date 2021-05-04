import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic


import window_ui_py.import_window_ui as import_window
from message_boxes import InfoBox


def dicts_distinction(first: dict, second: dict) -> bool:
    for key in first.keys():
        if first[key] != second[key]:
            return True

    return False


class CompareRecords(QDialog, import_window.Ui_import_window):
    replace_login_signal = pyqtSignal(str)
    add_new_login_signal = pyqtSignal(str, str)
    unconflict_record_signal = pyqtSignal(str)

    def __init__(self, first, second):
        super(CompareRecords, self).__init__()
        self.setupUi(self)
        self.first_dict = first
        self.second_dict = second
        self.changes_type = dict()
        self.login_names = self.set_login_names()
        self.__combo_box_val = 0
        self.combo_index = {'Replace': 0, 'Add': 1, 'Nothing': 2}
        self.submit_button.clicked.connect(self.process_submit_signal)
        self.combo_box.activated.connect(self.process_combo_box)

    @property
    def combo_box_val(self):
        return self.__combo_box_val

    @combo_box_val.setter
    def combo_box_val(self, value: str):
        self.__combo_box_val = value

    def set_login_names(self):
        first_temp = set(self.first_dict)
        second_temp = set(self.second_dict)
        login_names = first_temp.intersection(second_temp)

        return login_names

    def start_comparison(self):
        global key
        first = set(self.first_dict)
        second = set(self.second_dict)
        diff_records = second.difference(first)
        for key in diff_records:
            self.unconflict_record_signal.emit(key)
        for key in self.login_names:
            first = self.first_dict[key]
            second = self.second_dict[key]
            self.distinctions = dicts_distinction(first, second)

            if not self.distinctions:
                continue
            else:
                if not self.all_records.isChecked():
                    self.process_conflict()
                elif self.all_records.isChecked():
                    self.serialize_combo_value()

    def process_conflict(self):
        warning = f"You have a conflict \nin '{key}' record."
        conflict_title = f"'{key}' conflict"
        self.warning_label.setText(warning)
        self.setWindowTitle(conflict_title)
        self.adjustSize()
        self.setModal(True)
        self.exec_()

    def serialize_combo_value(self):
        if self.combo_box_val == self.combo_index['Nothing']:
            pass
        if self.combo_box_val == self.combo_index['Replace']:
            self.replace_login_signal.emit(key)
        if self.combo_box_val == self.combo_index['Add']:
            if self.all_records.isChecked():
                self.add_new_login_signal.emit(key, f"'{key}' New Name")
            else:
                self.add_new_login_signal.emit(key, "New Record Name")
        
    def process_submit_signal(self):
        self.serialize_combo_value()
        self.close()

    def process_combo_box(self, index):
        self.combo_box_val = index        
