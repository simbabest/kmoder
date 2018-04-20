# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xsd.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_XSD(object):
    def setupUi(self, XSD):
        XSD.setObjectName("XSD")
        XSD.resize(957, 732)
        XSD.setWindowOpacity(1.0)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(XSD)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(XSD)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(XSD)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(XSD)
        QtCore.QMetaObject.connectSlotsByName(XSD)

    def retranslateUi(self, XSD):
        _translate = QtCore.QCoreApplication.translate
        XSD.setWindowTitle(_translate("XSD", "相似度"))
        self.pushButton.setText(_translate("XSD", "相似度矩阵"))

