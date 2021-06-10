import ast
import json
import pickle
import os
import re
import io
import sys
import threading
import time
import requests

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tqdm import tqdm

import window_ui_py.drive_export_window_py as drive_export
from import_export.remote.drive_connect import DriveConnect
from import_export.remote.drive_folder import UserDriveFolder


class ListItem(QWidget):
    click_item_signal = pyqtSignal(str, str)

    def __init__(self, index, name, parent=None):
        super(ListItem, self).__init__(parent)

        self.textQVBoxLayout = QVBoxLayout()
        self.widget_label = QLabel()
        self.textQVBoxLayout.addWidget(self.widget_label)
        self.textQVBoxLayout.setGeometry(QRect(100, 200, 200, 200))
        self.setLayout(self.textQVBoxLayout)

        self.name = name
        self.id = index

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.click_item_signal.emit(self.id, self.name)

class DriveImport(QDialog, drive_export.Ui_drive_window):
    file_content_signal = pyqtSignal(dict)
    # finished = pyqtSignal(str)

    def __init__(self):
        super(DriveImport, self).__init__()
        self.setupUi(self)
        self.drive_conn = DriveConnect(standart_scope=False)
        self.service = self.drive_conn.service
        self.user_folder = UserDriveFolder()
        self.file_data = str()
        self.clicked_filename = ''

    def init_functionality(self):
        self.submit_button.clicked.connect(self.submit_user_choose)
        self.init_file_list()
        self.exec_()

    def init_file_list(self):
        if self.service:
            folder_content = self.user_folder.folder_content()
            order_number = 1
            for file_pair in folder_content:
                name = file_pair[-1]
                index = file_pair[0]
                temp = ListItem(index, name)
                item_name = f"{order_number}. {name}"
                temp.widget_label.setText(item_name)
                temp.widget_label.setStyleSheet("QLabel {\n"
                                    "font: 11pt \"Fira Sans Semi-Light\";\n"
                                    "}")
                temp.click_item_signal.connect(self.show_file_content)
                temp_list_widget = QListWidgetItem(self.files_list)
                temp_list_widget.setSizeHint(temp.sizeHint())
                self.files_list.addItem(temp_list_widget)
                self.files_list.setItemWidget(temp_list_widget, temp)
                order_number += 1

    def output_content(self):
        self.file_overview_stack.setCurrentIndex(1)
        # self.adjustSize()

    def submit_user_choose(self):
        if self.file_data:
            result = dict(ast.literal_eval(self.file_data))
            self.file_content_signal.emit(result)

    def close_content(self):
        self.file_overview_stack.setCurrentIndex(0)


    def show_file_content(self, file_id, file_name):
        self.service.permissions().create(body={"role": "reader", "type": "anyone"}, fileId=file_id).execute()
        download_thread = threading.Thread(target=self.download_file_from_google_drive, args=(file_id, file_name))
        download_thread.start()
        try:
            self.file_data = self.read_user_data(file_name)
        except FileNotFoundError:
            time.sleep(2)
            self.file_data = self.read_user_data(file_name)

        if file_name != self.clicked_filename and self.clicked_filename != '':
            os.remove(self.clicked_filename)
        self.clicked_filename = file_name

        self.file_content.setText(self.file_data)
        self.output_content()

    def read_user_data(self, file_name):
        with open(file_name, 'r') as stream:
            obj = json.load(stream)
  
            pretty_json = json.dumps(obj, indent=4)
        
        return pretty_json

    def download_file_from_google_drive(self, id, destination):
        def get_confirm_token(response):
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    return value
            return None

        def save_response_content(response, destination):
            CHUNK_SIZE = 32768
            # get the file size from Content-length response header
            file_size = int(response.headers.get("Content-Length", 0))
            # extract Content disposition from response headers
            content_disposition = response.headers.get("content-disposition")
            # parse filename
            filename = re.findall("filename=\"(.+)\"", content_disposition)[0]
            progress = tqdm(response.iter_content(CHUNK_SIZE), f"Downloading {filename}", total=file_size, unit="Byte", unit_scale=True, unit_divisor=1024)
            with open(destination, "wb") as f:
                for chunk in progress:
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        # update the progress bar
                        progress.update(len(chunk))
            progress.close()

        # base URL for download
        URL = "https://docs.google.com/uc?export=download"
        # init a HTTP session
        session = requests.Session()
        # make a request
        response = session.get(URL, params = {'id': id}, stream=True)
        # get confirmation token
        token = get_confirm_token(response)
        if token:
            params = {'id': id, 'confirm':token}
            response = session.get(URL, params=params, stream=True)
        # download to disk
        save_response_content(response, destination)
