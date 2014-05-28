# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ZeroFeeder.ui'
#
# Created: Mon Sep 09 13:30:40 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(351, 192)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(351, 192))
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "ZeroFeeder", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../vista 5728 icons/netcenter.dll_I0007_0409.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionFeed = QtGui.QAction(MainWindow)
        self.actionFeed.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../vista 5728 icons/netcenter.dll_I01f8_0409.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../vista 5728 icons/netcenter.dll_I0007_0409.ico")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionFeed.setIcon(icon1)
        self.actionFeed.setText(QtGui.QApplication.translate("MainWindow", "feed", None, QtGui.QApplication.UnicodeUTF8))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lao UI"))
        font.setPointSize(10)
        self.actionFeed.setFont(font)
        self.actionFeed.setObjectName(_fromUtf8("actionFeed"))
        self.toolBar.addAction(self.actionFeed)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionFeed, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), MainWindow.slot_ToggleFeed)
        QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL(_fromUtf8("cellDoubleClicked(int,int)")), MainWindow.slot_StartXingDlg)
        QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL(_fromUtf8("cellDoubleClicked(int,int)")), MainWindow.slot_CheckCybosStarter)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

