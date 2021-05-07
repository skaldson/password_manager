from __future__ import print_function
import pickle
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

from db_files.db_cursor import DBCursor
from import_export import generate_json


class DriveConnect:
    def __init__(self, standart_scope=True):
        self.standart_scope = standart_scope
        self.SCOPES = self.serialize_scope()
        self.__service = self.get_gdrive_service()

    def serialize_scope(self):
        if self.standart_scope:
            return ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']
        else:
            return ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file']

    @property
    def service(self):
        return self.__service

    def get_gdrive_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # return Google Drive API service
        return build('drive', 'v3', credentials=creds)

    def search(self, service, query):
        # search for the file
            result = []
            page_token = None
            while True:
                response = service.files().list(q=query,
                                                spaces="drive",
                                                fields="nextPageToken, files(id, name)",
                                                pageToken=page_token).execute()
                # iterate over filtered files
                for file in response.get("files", []):
                    result.append((file["id"], file["name"]))
                page_token = response.get('nextPageToken', None)
                if not page_token:
                    # no more files
                    break
            return result

def create_list(data, index):
    result = []
    for i in data:
        result.append(i[index])

    return result


class UserDriveFolder:
    def __init__(self):
        self.drive_conn = DriveConnect()
        self.service = self.drive_conn.service
        self.__folder_name = "PasswordManagerApp"
        self.__folder_type = "application/vnd.google-apps.folder"

    @property
    def folder_name(self):
        return self.__folder_name

    @property
    def folder_type(self):
        return self.__folder_type

    def is_folder_exist(self):
        if self.service:
            query = f"mimeType='{self.folder_type}'"
            search_result = self.drive_conn.search(self.service, query)

            folder_list = create_list(search_result, -1)
            id_list = create_list(search_result, 0)

            if self.folder_name in folder_list:
                index = folder_list.index(self.folder_name)
                self.folder_id = id_list[index]
                return True
            else:
                return False

    def folder_content(self):
        folder_exist = self.is_folder_exist()
        if folder_exist:
            query = f"'{self.folder_id}' in parents"
            folder_files = self.drive_conn.search(self.service, query)
            # folder_files = create_list(folder_files, -1)
            return folder_files
        else:
            return False


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
