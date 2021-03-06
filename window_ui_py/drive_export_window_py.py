# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './window_ui/drive_export_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_drive_window(object):
    def setupUi(self, drive_window):
        drive_window.setObjectName("drive_window")
        drive_window.resize(536, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./window_ui/../images/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        drive_window.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(drive_window)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.files_list = QtWidgets.QListWidget(drive_window)
        self.files_list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.files_list.setObjectName("files_list")
        self.horizontalLayout.addWidget(self.files_list)
        self.scroll_area = QtWidgets.QScrollArea(drive_window)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 248, 236))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.file_overview_stack = QtWidgets.QStackedWidget(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        self.file_overview_stack.setFont(font)
        self.file_overview_stack.setObjectName("file_overview_stack")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.file_overview_stack.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.file_content = QtWidgets.QLabel(self.page_2)
        self.file_content.setObjectName("file_content")
        self.verticalLayout.addWidget(self.file_content)
        self.file_overview_stack.addWidget(self.page_2)
        self.horizontalLayout_3.addWidget(self.file_overview_stack)
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scroll_area)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.submit_button = QtWidgets.QPushButton(drive_window)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.submit_button.setFont(font)
        self.submit_button.setObjectName("submit_button")
        self.verticalLayout_2.addWidget(self.submit_button)

        self.retranslateUi(drive_window)
        QtCore.QMetaObject.connectSlotsByName(drive_window)

    def retranslateUi(self, drive_window):
        _translate = QtCore.QCoreApplication.translate
        drive_window.setWindowTitle(_translate("drive_window", "Drive Import"))
        self.file_content.setText(_translate("drive_window", "TextLabel"))
        self.submit_button.setText(_translate("drive_window", "Submit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    drive_window = QtWidgets.QDialog()
    ui = Ui_drive_window()
    ui.setupUi(drive_window)
    drive_window.show()
    sys.exit(app.exec_())
