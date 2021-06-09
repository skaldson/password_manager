import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class DriveConnect:
    __token_file = 'token.pickle'
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

    @property
    def token(self):
        return self.__token_file

    def get_gdrive_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token):
            with open(self.token, 'rb') as token:
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
            with open(self.token, 'wb') as token:
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


    @classmethod
    def remove_token(cls):
        if os.path.exists(cls.__token_file):
            os.remove(cls.__token_file)
