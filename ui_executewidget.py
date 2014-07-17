# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'executewidget.ui'
#
# Created: Thu Jul 17 00:37:55 2014
#      by: PyQt4 UI code generator 4.9.6
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
        Form.resize(246, 105)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelPrice = QtGui.QLabel(Form)
        self.labelPrice.setObjectName(_fromUtf8("labelPrice"))
        self.gridLayout.addWidget(self.labelPrice, 1, 0, 1, 1)
        self.doubleSpinBoxPrice = QtGui.QDoubleSpinBox(Form)
        self.doubleSpinBoxPrice.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxPrice.setSingleStep(0.01)
        self.doubleSpinBoxPrice.setObjectName(_fromUtf8("doubleSpinBoxPrice"))
        self.gridLayout.addWidget(self.doubleSpinBoxPrice, 1, 1, 1, 1)
        self.lineEditShortCode = QtGui.QLineEdit(Form)
        self.lineEditShortCode.setText(_fromUtf8(""))
        self.lineEditShortCode.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditShortCode.setObjectName(_fromUtf8("lineEditShortCode"))
        self.gridLayout.addWidget(self.lineEditShortCode, 0, 1, 1, 1)
        self.labelShortCode = QtGui.QLabel(Form)
        self.labelShortCode.setObjectName(_fromUtf8("labelShortCode"))
        self.gridLayout.addWidget(self.labelShortCode, 0, 0, 1, 1)
        self.labelQty = QtGui.QLabel(Form)
        self.labelQty.setObjectName(_fromUtf8("labelQty"))
        self.gridLayout.addWidget(self.labelQty, 2, 0, 1, 1)
        self.spinBoxQty = QtGui.QSpinBox(Form)
        self.spinBoxQty.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxQty.setObjectName(_fromUtf8("spinBoxQty"))
        self.gridLayout.addWidget(self.spinBoxQty, 2, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pushButtonSend = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSend.sizePolicy().hasHeightForWidth())
        self.pushButtonSend.setSizePolicy(sizePolicy)
        self.pushButtonSend.setObjectName(_fromUtf8("pushButtonSend"))
        self.verticalLayout_2.addWidget(self.pushButtonSend)
        self.groupBoxBuySell = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxBuySell.sizePolicy().hasHeightForWidth())
        self.groupBoxBuySell.setSizePolicy(sizePolicy)
        self.groupBoxBuySell.setTitle(_fromUtf8(""))
        self.groupBoxBuySell.setObjectName(_fromUtf8("groupBoxBuySell"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBoxBuySell)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radioButtonBuy = QtGui.QRadioButton(self.groupBoxBuySell)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButtonBuy.sizePolicy().hasHeightForWidth())
        self.radioButtonBuy.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.radioButtonBuy.setFont(font)
        self.radioButtonBuy.setChecked(True)
        self.radioButtonBuy.setObjectName(_fromUtf8("radioButtonBuy"))
        self.verticalLayout.addWidget(self.radioButtonBuy)
        self.radioButtonSell = QtGui.QRadioButton(self.groupBoxBuySell)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButtonSell.sizePolicy().hasHeightForWidth())
        self.radioButtonSell.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.radioButtonSell.setFont(font)
        self.radioButtonSell.setObjectName(_fromUtf8("radioButtonSell"))
        self.verticalLayout.addWidget(self.radioButtonSell)
        self.verticalLayout_2.addWidget(self.groupBoxBuySell)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.labelPrice.setBuddy(self.doubleSpinBoxPrice)
        self.labelShortCode.setBuddy(self.lineEditShortCode)
        self.labelQty.setBuddy(self.spinBoxQty)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEditShortCode, self.doubleSpinBoxPrice)
        Form.setTabOrder(self.doubleSpinBoxPrice, self.spinBoxQty)
        Form.setTabOrder(self.spinBoxQty, self.radioButtonBuy)
        Form.setTabOrder(self.radioButtonBuy, self.radioButtonSell)
        Form.setTabOrder(self.radioButtonSell, self.pushButtonSend)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.labelPrice.setText(_translate("Form", "Price", None))
        self.labelShortCode.setText(_translate("Form", "ShortCode", None))
        self.labelQty.setText(_translate("Form", "Qty", None))
        self.pushButtonSend.setText(_translate("Form", "Sell", None))
        self.radioButtonBuy.setText(_translate("Form", "Buy", None))
        self.radioButtonSell.setText(_translate("Form", "Sell", None))

