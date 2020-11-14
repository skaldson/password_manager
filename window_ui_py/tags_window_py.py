# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './window_ui/tags_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tags_window(object):
    def setupUi(self, tags_window):
        tags_window.setObjectName("tags_window")
        tags_window.resize(364, 254)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(tags_window)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(100, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.delete_button = QtWidgets.QToolButton(tags_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.delete_button.setFont(font)
        self.delete_button.setStyleSheet("")
        self.delete_button.setIconSize(QtCore.QSize(16, 16))
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout_2.addWidget(self.delete_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.tag_label = QtWidgets.QLabel(tags_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tag_label.setFont(font)
        self.tag_label.setObjectName("tag_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tag_label)
        self.tag_name = QtWidgets.QLineEdit(tags_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tag_name.setFont(font)
        self.tag_name.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.tag_name.setInputMethodHints(QtCore.Qt.ImhLatinOnly|QtCore.Qt.ImhPreferLatin)
        self.tag_name.setMaxLength(14)
        self.tag_name.setClearButtonEnabled(True)
        self.tag_name.setObjectName("tag_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tag_name)
        self.horizontalLayout.addLayout(self.formLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(48, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.colour_layout = QtWidgets.QGridLayout()
        self.colour_layout.setObjectName("colour_layout")
        self.verticalLayout_3.addLayout(self.colour_layout)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.tag_submit = QtWidgets.QPushButton(tags_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tag_submit.setFont(font)
        self.tag_submit.setObjectName("tag_submit")
        self.verticalLayout_2.addWidget(self.tag_submit)

        self.retranslateUi(tags_window)
        QtCore.QMetaObject.connectSlotsByName(tags_window)

    def retranslateUi(self, tags_window):
        _translate = QtCore.QCoreApplication.translate
        tags_window.setWindowTitle(_translate("tags_window", "Add Tag"))
        self.delete_button.setText(_translate("tags_window", "Del"))
        self.tag_label.setText(_translate("tags_window", "Tag Name"))
        self.tag_submit.setText(_translate("tags_window", "Submit"))
