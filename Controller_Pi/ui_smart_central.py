# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/icer/Documents/github/Smart-Home-Audio-System/Controller_Pi/smart_central.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(590, 10, 191, 241))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 40, 191, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 100, 191, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_5.setGeometry(QtCore.QRect(0, 160, 191, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(300, 10, 281, 451))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 300, 140, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 250, 81, 50))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 250, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.groupBox_2)
        self.graphicsView_2.setGeometry(QtCore.QRect(0, 30, 250, 210))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(0, 30, 291, 210))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("images/diningroom.png"))
        self.label_6.setScaledContents(False)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.music_label_status_2 = QtWidgets.QLabel(self.groupBox_2)
        self.music_label_status_2.setGeometry(QtCore.QRect(170, 300, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.music_label_status_2.setFont(font)
        self.music_label_status_2.setText("")
        self.music_label_status_2.setObjectName("music_label_status_2")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(10, 380, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.groupBox_2)
        self.lcdNumber_2.setGeometry(QtCore.QRect(160, 330, 111, 51))
        self.lcdNumber_2.setLineWidth(0)
        self.lcdNumber_2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(10, 340, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.music_track_name_label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.music_track_name_label_2.setGeometry(QtCore.QRect(100, 380, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.music_track_name_label_2.setFont(font)
        self.music_track_name_label_2.setText("")
        self.music_track_name_label_2.setObjectName("music_track_name_label_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 281, 451))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 300, 140, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(190, 250, 81, 50))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 250, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(0, 30, 281, 210))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("images/bedroom.png"))
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.music_label_status = QtWidgets.QLabel(self.groupBox)
        self.music_label_status.setGeometry(QtCore.QRect(170, 300, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.music_label_status.setFont(font)
        self.music_label_status.setObjectName("music_label_status")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 380, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.lcdNumber = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber.setGeometry(QtCore.QRect(170, 330, 111, 51))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.lcdNumber.setFont(font)
        self.lcdNumber.setLineWidth(0)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setObjectName("lcdNumber")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(10, 340, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.music_track_name_label = QtWidgets.QLabel(self.groupBox)
        self.music_track_name_label.setGeometry(QtCore.QRect(100, 380, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.music_track_name_label.setFont(font)
        self.music_track_name_label.setObjectName("music_track_name_label")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(590, 270, 191, 191))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_3.setTitle(_translate("Form", "Control "))
        self.pushButton_3.setText(_translate("Form", "Reset"))
        self.pushButton_4.setText(_translate("Form", "Connect"))
        self.pushButton_5.setText(_translate("Form", "Clear Meassage"))
        self.groupBox_2.setTitle(_translate("Form", "Living room"))
        self.label_3.setText(_translate("Form", "Track status:"))
        self.pushButton_2.setText(_translate("Form", "OFF"))
        self.label_4.setText(_translate("Form", "Light:"))
        self.label_8.setText(_translate("Form", "Track:"))
        self.label_10.setText(_translate("Form", "Volume:"))
        self.groupBox.setTitle(_translate("Form", "Bedroom"))
        self.label.setText(_translate("Form", "Track status:"))
        self.pushButton.setText(_translate("Form", "OFF"))
        self.label_2.setText(_translate("Form", "Light:"))
        self.music_label_status.setText(_translate("Form", " "))
        self.label_7.setText(_translate("Form", "Track:"))
        self.label_9.setText(_translate("Form", "Volume:"))
        self.music_track_name_label.setText(_translate("Form", " "))

