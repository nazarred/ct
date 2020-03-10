# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1042, 848)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.clicked.connect
        self.pushButton.setGeometry(QtCore.QRect(540, 360, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 429, 1021, 371))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutMap = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutMap.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutMap.setObjectName("verticalLayoutMap")
        self.tabWidgetInputCrs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidgetInputCrs.setGeometry(QtCore.QRect(11, 11, 511, 311))
        self.tabWidgetInputCrs.setObjectName("tabWidgetInputCrs")
        self.tabCompoundCrs = QtWidgets.QWidget()
        self.tabCompoundCrs.setObjectName("tabCompoundCrs")
        self.tabWidgetInputCrs.addTab(self.tabCompoundCrs, "")
        self.tabCrsHV = QtWidgets.QWidget()
        self.tabCrsHV.setObjectName("tabCrsHV")
        self.label = QtWidgets.QLabel(self.tabCrsHV)
        self.label.setGeometry(QtCore.QRect(9, 9, 76, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tabCrsHV)
        self.label_2.setGeometry(QtCore.QRect(467, 9, 53, 17))
        self.label_2.setObjectName("label_2")
        self.comboBoxCrsH = QtWidgets.QComboBox(self.tabCrsHV)
        self.comboBoxCrsH.addItem()
        self.comboBoxCrsH.setGeometry(QtCore.QRect(10, 40, 201, 31))
        self.comboBoxCrsH.setEditable(True)
        self.comboBoxCrsH.setObjectName("comboBoxCrsH")
        self.comboBoxCrsV = QtWidgets.QComboBox(self.tabCrsHV)
        self.comboBoxCrsV.setGeometry(QtCore.QRect(230, 40, 191, 31))
        self.comboBoxCrsV.setEditable(True)
        self.comboBoxCrsV.setObjectName("comboBoxCrsV")
        self.tabWidgetInputCrs.addTab(self.tabCrsHV, "")
        self.tabCrsText = QtWidgets.QWidget()
        self.tabCrsText.setObjectName("tabCrsText")
        self.tabWidgetInputCrs.addTab(self.tabCrsText, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1042, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidgetInputCrs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.tabWidgetInputCrs.setTabText(self.tabWidgetInputCrs.indexOf(self.tabCompoundCrs), _translate("MainWindow", "Compound / Geographic 3D"))
        self.label.setText(_translate("MainWindow", "Horizontall"))
        self.label_2.setText(_translate("MainWindow", "Vertival"))
        self.tabWidgetInputCrs.setTabText(self.tabWidgetInputCrs.indexOf(self.tabCrsHV), _translate("MainWindow", "Horizontal & Vertical CRS"))
        self.tabWidgetInputCrs.setTabText(self.tabWidgetInputCrs.indexOf(self.tabCrsText), _translate("MainWindow", "WKT"))

