import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import window_ui_py.local_import_py as local_import


class LocalImport(QDialog, local_import.Ui_local_import):
    accept_signal = pyqtSignal()
    
    def __init__(self, file_content):
        super(LocalImport, self).__init__()
        self.setupUi(self)
        self.content = file_content

    def init_functionality(self):
        self.accept_button.clicked.connect(self.accept_content)
        self.set_content()
        self.show()

    def set_content(self):
        result_str = str()
        for login_name, login_dict in self.content.items():
            result_str += "<font size=5>Record: %s</font><br>" % login_name
            tag_str = ''
            for key, value in login_dict.items():
                if key != 'colours' and key != 'tags':
                    data_tuple = (key, value)
                    result_str += "<font size=4>%s: %s</font><br>" % data_tuple
                if key == 'tags':
                    result_str += "<font size=4>%s: </font>" % key
                    for i in value:
                        colour = login_dict['colours'][value.index(i)]
                        temp_str = "<font size=4 color='%s'>%s </font>" % (colour, i)
                        tag_str += temp_str
            result_str += tag_str + "<br><br>"
        self.file_content.setText(result_str)

    def accept_content(self):
        self.accept_signal.emit()
        self.close()
