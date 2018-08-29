# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xinglogindlg.ui'
#
# Created: Thu Jun 20 09:46:13 2013
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
        dialog.resize(287, 220)
        dialog.setMinimumSize(QtCore.QSize(287, 220))
        dialog.setMaximumSize(QtCore.QSize(287, 220))
        dialog.setWindowTitle(QtGui.QApplication.translate("dialog", "Login", None, QtGui.QApplication.UnicodeUTF8))
        dialog.setModal(True)
        self.layoutWidget = QtGui.QWidget(dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 240, 186))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setText(QtGui.QApplication.translate("dialog", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setText(QtGui.QApplication.translate("dialog", "ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setText(QtGui.QApplication.translate("dialog", "PassWord:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setText(QtGui.QApplication.translate("dialog", "Server Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEditEtradeServerName = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditEtradeServerName.setText(_fromUtf8(""))
        self.lineEditEtradeServerName.setObjectName(_fromUtf8("lineEditEtradeServerName"))
        self.gridLayout.addWidget(self.lineEditEtradeServerName, 0, 1, 1, 1)
        self.lineEditId = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditId.setObjectName(_fromUtf8("lineEditId"))
        self.gridLayout.addWidget(self.lineEditId, 1, 1, 1, 1)
        self.lineEditPassword = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditPassword.setInputMask(_fromUtf8(""))
        self.lineEditPassword.setText(_fromUtf8(""))
        self.lineEditPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditPassword.setObjectName(_fromUtf8("lineEditPassword"))
        self.gridLayout.addWidget(self.lineEditPassword, 2, 1, 1, 1)
        self.comboBoxServerType = QtGui.QComboBox(self.layoutWidget)
        self.comboBoxServerType.setEditable(False)
        self.comboBoxServerType.setObjectName(_fromUtf8("comboBoxServerType"))
        self.comboBoxServerType.addItem(_fromUtf8(""))
        self.comboBoxServerType.setItemText(0, QtGui.QApplication.translate("dialog", "real server", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxServerType.addItem(_fromUtf8(""))
        self.comboBoxServerType.setItemText(1, QtGui.QApplication.translate("dialog", "demo server", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.comboBoxServerType, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButtonLogin = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLogin.sizePolicy().hasHeightForWidth())
        self.pushButtonLogin.setSizePolicy(sizePolicy)
        self.pushButtonLogin.setMaximumSize(QtCore.QSize(283, 16777215))
        self.pushButtonLogin.setText(QtGui.QApplication.translate("dialog", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLogin.setObjectName(_fromUtf8("pushButtonLogin"))
        self.verticalLayout.addWidget(self.pushButtonLogin)
        self.pushButtonTest = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonTest.setText(QtGui.QApplication.translate("dialog", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTest.setObjectName(_fromUtf8("pushButtonTest"))
        self.verticalLayout.addWidget(self.pushButtonTest)
        self.lineEditMessage = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditMessage.setReadOnly(True)
        self.lineEditMessage.setObjectName(_fromUtf8("lineEditMessage"))
        self.verticalLayout.addWidget(self.lineEditMessage)
        self.label.setBuddy(self.lineEditEtradeServerName)
        self.label_2.setBuddy(self.lineEditId)
        self.label_3.setBuddy(self.lineEditPassword)

        self.retranslateUi(dialog)
        QtCore.QObject.connect(self.pushButtonLogin, QtCore.SIGNAL(_fromUtf8("clicked()")), dialog.slot_login)
        QtCore.QObject.connect(self.pushButtonTest, QtCore.SIGNAL(_fromUtf8("clicked()")), dialog.slot_test)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        dialog.setTabOrder(self.lineEditEtradeServerName, self.lineEditId)
        dialog.setTabOrder(self.lineEditId, self.lineEditPassword)
        dialog.setTabOrder(self.lineEditPassword, self.comboBoxServerType)
        dialog.setTabOrder(self.comboBoxServerType, self.pushButtonLogin)
        dialog.setTabOrder(self.pushButtonLogin, self.lineEditMessage)

    def retranslateUi(self, dialog):
        pass

