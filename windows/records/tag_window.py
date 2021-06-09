import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic

import window_ui_py.tags_window_py as tags_window
from db_files.db_cursor import DBCursor
from windows.utility.message_boxes import InfoBox
from windows.correct_input import delete_rspace


class TagWindow(QDialog, tags_window.Ui_tags_window):

    add_tag_signal = pyqtSignal(str, int)
    edit_tag_signal = pyqtSignal(str, int)

    def __init__(self):
        super(TagWindow, self).__init__()
        self.setupUi(self)
        self.db_cursor = DBCursor.getInstance()
        self.init_colour_layout()
        self.init_functionality()

    def edit_mode(self, current_tag):
        self.setModal(True)
        self.setWindowTitle('Edit Tag')
        self.tag_submit.clicked.connect(self.edit_tag_mode)

        tag_name = current_tag[0]
        x_pos, y_pos = current_tag[-1]//3, current_tag[-1]%3
        self.tag_name.setText(tag_name)
        
        colour = current_tag[-1] + 1
        colour = (self.db_cursor.get_colour_by_id(colour))[0][0]
        self.set_colour_button(x_pos, y_pos, colour, is_checked=True)
        
        self.show()


    def init_functionality(self):
        only_text = QRegExp('[a-z-A-Z_]+')
        validator = QRegExpValidator(only_text)
        self.tag_name.setValidator(validator)

        self.tag_submit.clicked.connect(self.add_tag_mode)

    def set_colour_button(self, x_pos, y_pos, colour, is_checked=False):
        temp = QRadioButton()
        temp.setChecked(True) if is_checked == True else temp.setChecked(False)

        temp.setStyleSheet("""QRadioButton {
                            height: 40px; width: 75px;
                            background-color: %s;
                            border-radius: 8px;}""" % (colour))
        self.colors_dict[temp] = colour
        self.colour_layout.addWidget(temp, x_pos, y_pos)

    def init_colour_layout(self):
        self.colors_list = self.db_cursor.get_colors
        self.colour_layout.setColumnStretch(1, 4)
        self.colour_layout.setColumnStretch(2, 4)

        self.colors_dict = {}
        colour_index = 0
        for x_pos in range((len(self.colors_list) // 3) + 1):
            for y_pos in range(3):
                if colour_index == len(self.colors_list):
                    break
                else:
                    temp_colour = self.colors_list[colour_index]
                    self.set_colour_button(x_pos, y_pos, temp_colour[0])
                colour_index += 1

    def init_tag_data(self, signal):
        selected_colour = None
        for k, v in self.colors_dict.items():
            if k.isChecked():
                selected_colour = (self.db_cursor.get_colour_by_name(v))[0][0]

        tag_name = delete_rspace(self.tag_name.text())
        
        if selected_colour:
            if len(tag_name) < 4:
                InfoBox(self, 'Tag name must be at least 4 characters long')
            else:
                signal.emit(tag_name, selected_colour)

    def add_tag_mode(self):
        self.init_tag_data(self.add_tag_signal)

    def edit_tag_mode(self):
        self.init_tag_data(self.edit_tag_signal)
