from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import window_ui_py.edit_section_py as edit_section
from db_files.db_cursor import DBCursor
from tag_info import TagInfo
from password_edit import PasswordEdit
from record_abs_class import RecordAbsClass


class EditSection(QWidget, edit_section.Ui_Form):

    submit_signal = pyqtSignal(str, str, bytes, bytes, bytes, list)

    def __init__(self, parent=None):
        super(EditSection, self).__init__()
        self.setupUi(self)

        self.scroll_tag_area.setWidget(self.tag_widget)
        self.sudmit_editing.clicked.connect(self.submit_edit)
        self.tag_widget.set_edit_section_mode()
        self.db_cursor = DBCursor.getInstance()
        self.record_name = ''
        # self.main_key = str()
        # self.user_id = int()

        self.password_row()
        self.init_tags()
        self.premordial_list = []

    
    def password_row(self):
        self.password = PasswordEdit(self)
        self.password.set_style()
        self.pass_label = QLabel('Password')
        self.pass_label.setFont(QFont('Fira Sans Semi-Light', 12))

        self.data_layout.addRow(self.pass_label, self.password)

    def get_forms_values(self):
        tags = self.tag_widget.pressed_tags
        login_name, login = self.login_name.text(), self.login.text()
        password = self.password.text()

        return [tags, login_name, login, password]

    def premordial_values(self):
        self.prem_tags, self.prem_login_name, self.prem_login, self.prem_password = self.get_forms_values()
       
        return [self.prem_tags, self.prem_login_name, self.prem_login, self.prem_password]
    
    def init_record_name(self, record_name):
        self.record_name = record_name

    def init_tags(self):
        self.tag_widget.reinit_tags()
        marked_tags = self.db_cursor.get_tags_by_login_name(self.record_name)
        tag_names = [i[0] for i in marked_tags]
        
        nonmarked_tags = self.db_cursor.get_special_tag_and_colour(tag_names)
        result_tags_list = marked_tags + nonmarked_tags
        for i in result_tags_list:
            temp_tag_info = TagInfo()
            if i in marked_tags:
                temp_tag_info.pressed_state = True
                temp_tag_info.tag_description = {'colour': i[-1]}
                self.tag_widget.tags = (i[0], temp_tag_info)
            else:
                temp_tag_info.tag_description = {'colour': i[-1]}
                self.tag_widget.tags = (i[0], temp_tag_info)
        self.tag_widget.repaint()


    def submit_edit(self):
        tags, login_name, login, password = self.get_forms_values()

        abstract_record = RecordAbsClass(self, login_name, login, password, tags)
        result_dict = abstract_record.result_forms_dict(edit_section=True)
        
        if result_dict:
            result_list = self.get_forms_values()
            result_login, result_password = result_dict['login'], result_dict['password']
            urandom = result_dict['urandom']
             
            if result_list == self.premordial_list:
                pass
            else:
                self.submit_signal.emit(self.premordial_list[1], login_name, result_login, result_password, urandom, tags)
