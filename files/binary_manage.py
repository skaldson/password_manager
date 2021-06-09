import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def convert_into_binary(file_name):
    converted_data = 0
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as file_stream:
            converted_data = file_stream.read()

        return converted_data
    else:
        return 0

def binary_to_file(data, file):
    with open(file, 'wb') as bin_stream:
        bin_stream.write(data)

def set_user_photo(photo, obj, new_photo=False):
    user_photo = photo
    file_name = './temp_image'
    try:
        if not new_photo:
            if not user_photo:
                button_icon = QIcon()
                obj.setIcon(button_icon)
            else:
                binary_to_file(user_photo, file_name)
                image_pixmap = QPixmap(file_name)
                button_icon = QIcon(image_pixmap)
                obj.setIcon(button_icon)
                obj.setIconSize(QSize(75,75))
                os.remove(file_name)
        else:
            image_pixmap = QPixmap(user_photo)
            button_icon = QIcon(image_pixmap)
            obj.setIcon(button_icon)
            obj.setIconSize(QSize(75,75))
    except TypeError:
        pass

def new_user_photo(main_window, photo_name, obj, second_attempt=False):
    file_dialog = QFileDialog()
    user_name = os.getlogin()
    folder_path = f"/home/{user_name}"

    if second_attempt:
        folder_path = second_attempt
    
    photo_name = file_dialog.getOpenFileName(main_window, "Open Image",
            folder_path, "Image Files (*.png *.jpg *jpeg *.bmp)")

    if photo_name[0]:
        set_user_photo(photo_name[0], obj, True)
        main_window.adjustSize()
        return photo_name
    else:
        return str()
