from import_export.remote.drive_connect import DriveConnect



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
            return folder_files
        else:
            return False
