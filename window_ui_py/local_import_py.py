# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './window_ui/local_import.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_local_import(object):
    def setupUi(self, local_import):
        local_import.setObjectName("local_import")
        local_import.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(local_import)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scroll_area = QtWidgets.QScrollArea(local_import)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 376, 242))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.file_content = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.file_content.setObjectName("file_content")
        self.verticalLayout_2.addWidget(self.file_content)
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scroll_area)
        self.accept_button = QtWidgets.QPushButton(local_import)
        self.accept_button.setObjectName("accept_button")
        self.verticalLayout.addWidget(self.accept_button)

        self.retranslateUi(local_import)
        QtCore.QMetaObject.connectSlotsByName(local_import)

    def retranslateUi(self, local_import):
        _translate = QtCore.QCoreApplication.translate
        local_import.setWindowTitle(_translate("local_import", "Local Import"))
        self.file_content.setText(_translate("local_import", "TextLabel"))
        self.accept_button.setText(_translate("local_import", "Accept"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    local_import = QtWidgets.QDialog()
    ui = Ui_local_import()
    ui.setupUi(local_import)
    local_import.show()
    sys.exit(app.exec_())
