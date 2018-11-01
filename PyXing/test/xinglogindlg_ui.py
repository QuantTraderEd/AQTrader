# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xinglogindlg.ui'
#
# Created: Sun Jun 09 15:18:22 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName(_fromUtf8("dialog"))
        dialog.resize(287, 192)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        dialog.setMinimumSize(QtCore.QSize(287, 192))
        dialog.setWindowTitle(QtGui.QApplication.translate("dialog", "XingLogin", None, QtGui.QApplication.UnicodeUTF8))
        self.widget = QtGui.QWidget(dialog)
        self.widget.setGeometry(QtCore.QRect(20, 20, 240, 157))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setText(QtGui.QApplication.translate("dialog", "ETrade Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setText(QtGui.QApplication.translate("dialog", "ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setText(QtGui.QApplication.translate("dialog", "PassWord:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setText(QtGui.QApplication.translate("dialog", "Server Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEditEtradeServerName = QtGui.QLineEdit(self.widget)
        self.lineEditEtradeServerName.setObjectName(_fromUtf8("lineEditEtradeServerName"))
        self.gridLayout.addWidget(self.lineEditEtradeServerName, 0, 1, 1, 1)
        self.lineEditId = QtGui.QLineEdit(self.widget)
        self.lineEditId.setObjectName(_fromUtf8("lineEditId"))
        self.gridLayout.addWidget(self.lineEditId, 1, 1, 1, 1)
        self.lineEditPassword = QtGui.QLineEdit(self.widget)
        self.lineEditPassword.setObjectName(_fromUtf8("lineEditPassword"))
        self.gridLayout.addWidget(self.lineEditPassword, 2, 1, 1, 1)
        self.comboBoxServerType = QtGui.QComboBox(self.widget)
        self.comboBoxServerType.setEditable(False)
        self.comboBoxServerType.setObjectName(_fromUtf8("comboBoxServerType"))
        self.comboBoxServerType.addItem(_fromUtf8(""))
        self.comboBoxServerType.setItemText(0, QtGui.QApplication.translate("dialog", "real server", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxServerType.addItem(_fromUtf8(""))
        self.comboBoxServerType.setItemText(1, QtGui.QApplication.translate("dialog", "demo server", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.comboBoxServerType, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButtonLogin = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLogin.sizePolicy().hasHeightForWidth())
        self.pushButtonLogin.setSizePolicy(sizePolicy)
        self.pushButtonLogin.setMaximumSize(QtCore.QSize(283, 16777215))
        self.pushButtonLogin.setText(QtGui.QApplication.translate("dialog", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLogin.setObjectName(_fromUtf8("pushButtonLogin"))
        self.verticalLayout.addWidget(self.pushButtonLogin)
        self.lineEditMessage = QtGui.QLineEdit(self.widget)
        self.lineEditMessage.setReadOnly(True)
        self.lineEditMessage.setObjectName(_fromUtf8("lineEditMessage"))
        self.verticalLayout.addWidget(self.lineEditMessage)
        self.label.setBuddy(self.lineEditEtradeServerName)
        self.label_2.setBuddy(self.lineEditId)
        self.label_3.setBuddy(self.lineEditPassword)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        dialog.setTabOrder(self.lineEditEtradeServerName, self.lineEditId)
        dialog.setTabOrder(self.lineEditId, self.lineEditPassword)
        dialog.setTabOrder(self.lineEditPassword, self.comboBoxServerType)
        dialog.setTabOrder(self.comboBoxServerType, self.pushButtonLogin)
        dialog.setTabOrder(self.pushButtonLogin, self.lineEditMessage)

    def retranslateUi(self, dialog):
        pass

