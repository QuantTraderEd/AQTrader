# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zeropositionviewer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(777, 146)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(3)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "PositionViewer", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ShortCD", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Qty", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Mark", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "TradePrice", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Delta", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Gamma", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Theta", None))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Vega", None))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Form", "P/L Open", None))

