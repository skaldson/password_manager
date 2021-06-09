from __future__ import print_function
import pickle
import os.path
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

from db_files.db_cursor import DBCursor
from import_export.local.local import generate_json
from import_export.remote.drive_connect import DriveConnect
from import_export.remote.drive_folder import UserDriveFolder


class DriveExport:
    def __init__(self):
        self.db_cursor = DBCursor.getInstance()
        self.__folder_type = "application/vnd.google-apps.folder"
        self.__folder_name = "PasswordManagerApp"
        self.__folder_metadata = {
            "name": f"{self.folder_name}",
            "mimeType": f"{self.folder_type}"
        }
        self.drive_conn = DriveConnect()
        self.service = self.drive_conn.service
        self.user_folder = UserDriveFolder()

    @property
    def folder_name(self):
        return self.__folder_name

    @property
    def folder_type(self):
        return self.__folder_type

    @property
    def folder_metadata(self):
        return self.__folder_metadata

    def init_functionality(self):
        self.import_remote_file()

    def import_remote_file(self):
        if self.service:
            is_folder_exist = self.user_folder.is_folder_exist()
            if is_folder_exist:
                file_name = generate_json()
                file_metadata = {
                                    "name": file_name,
                                    "parents": [self.user_folder.folder_id]
                                }
                media = MediaFileUpload(file_name, resumable=True)
                file = self.service.files()
                file = file.create(body=file_metadata, media_body=media, fields='id')
                file = file.execute()
                os.remove(file_name)
            else:
                print('created')
                self.create_remote_folder()

    def create_remote_folder(self):
        temp_fold = self.service.files()
        temp_fold = temp_fold.create(body=self.folder_metadata, fields="id")
        temp_fold = temp_fold.execute()
