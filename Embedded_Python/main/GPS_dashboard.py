# ---------------------------------------------------------------------------------------------------------
# @file		 SATELLITE BASED NAVIGATION DATA GUI.py
# @author	 Abhinaba Ghosh
# @date		 31/10/2022
# @brief	 QT based GUI for nmea data processing
# @attention Copyright (C) 2022 | PERSONAL
# @version   f{ver}
# ----------------------------------------------------------------------------------------------------------
ver = str('1.1.0')  # Update version number here.

# Module imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes
import time
import os
import sys
import re
import serial
import winsound
logfile = r"D:\EMBEDDED LATEST PROJECT BACKUP\GIT Platform\Project\Embedded_Python\main\nmea_log.txt"
BLUE = "\033[94m{}\033[00m"
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
logo = 'satellite.png'
splash_img = r'C:\Users\user\OneDrive\Pictures\sat.png'
comport = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10"]
baudrate = ["9600", "115200"]
global com, baud, LAT, LONG


class Ui_MainWindow(object):

    def __init__(self):
        super().__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(670, 708)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        QApplication.processEvents()

    def setupUi(self, MainWindow):
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1400, 1800))
        self.frame.setStyleSheet("background-color: rgb(85, 85, 127);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 1400, 1800))
        self.frame_2.setStyleSheet("background-color: rgb(0, 0, 127);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.messagebox = QtWidgets.QMessageBox(self.centralwidget)
        self.messagebox.setObjectName("messagebox")
        self.comboBox = QtWidgets.QComboBox(self.frame_2)
        self.comboBox.setGeometry(QtCore.QRect(280, 10, 71, 22))
        self.comboBox.setStyleSheet("background-color: rgb(85, 255, 255);\n"
        "color: rgb(0, 0, 0);\n"
        "font: 75 10pt \"Perpetua Titling MT\";")
        self.comboBox.setObjectName("comboBox")
        for options in comport:
                self.comboBox.addItem(options)
        self.comboBox_2 = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_2.setGeometry(QtCore.QRect(460, 10, 91, 22))
        self.comboBox_2.setStyleSheet("background-color: rgb(85, 255, 255);\n"
        "color: rgb(0, 0, 0);\n"
        "font: 75 10pt \"Perpetua Titling MT\";")
        self.comboBox_2.setObjectName("comboBox_2")
        for options in baudrate:
                self.comboBox_2.addItem(options)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(240, 10, 41, 21))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 6pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(410, 10, 41, 21))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 6pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 231, 41))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 6pt \"MS Sans Serif\";")
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(560, 10, 51, 21))
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 6pt \"MS Shell Dlg 2\";")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(610, 10, 61, 21))
        self.label_6.setStyleSheet("color: rgb(0, 255, 255);\n"
"font: 75 8pt \"MS Shell Dlg 2\";")
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(360, 10, 31, 21))
        self.pushButton.setMaximumSize(QtCore.QSize(31, 16777215))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 300, 651, 81))
        self.groupBox_2.setStyleSheet("color: rgb(170, 170, 0);")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_26 = QtWidgets.QLabel(self.groupBox_2)
        self.label_26.setGeometry(QtCore.QRect(10, 20, 191, 16))
        self.label_26.setObjectName("label_26")
        self.lineEdit_16 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_16.setGeometry(QtCore.QRect(220, 20, 41, 20))
        self.lineEdit_16.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.label_27 = QtWidgets.QLabel(self.groupBox_2)
        self.label_27.setGeometry(QtCore.QRect(10, 50, 211, 16))
        self.label_27.setObjectName("label_27")
        self.lineEdit_17 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_17.setGeometry(QtCore.QRect(220, 50, 41, 20))
        self.lineEdit_17.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.label_28 = QtWidgets.QLabel(self.groupBox_2)
        self.label_28.setGeometry(QtCore.QRect(270, 20, 161, 16))
        self.label_28.setObjectName("label_28")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_18.setGeometry(QtCore.QRect(440, 20, 201, 20))
        self.lineEdit_18.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.label_29 = QtWidgets.QLabel(self.groupBox_2)
        self.label_29.setGeometry(QtCore.QRect(270, 50, 31, 16))
        self.label_29.setObjectName("label_29")
        self.lineEdit_19 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_19.setGeometry(QtCore.QRect(310, 50, 61, 20))
        self.lineEdit_19.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_19.setText("")
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.label_30 = QtWidgets.QLabel(self.groupBox_2)
        self.label_30.setGeometry(QtCore.QRect(400, 50, 31, 16))
        self.label_30.setObjectName("label_30")
        self.lineEdit_20 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_20.setGeometry(QtCore.QRect(440, 50, 71, 20))
        self.lineEdit_20.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_20.setText("")
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.label_31 = QtWidgets.QLabel(self.groupBox_2)
        self.label_31.setGeometry(QtCore.QRect(520, 50, 31, 16))
        self.label_31.setObjectName("label_31")
        self.lineEdit_21 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_21.setGeometry(QtCore.QRect(570, 50, 71, 20))
        self.lineEdit_21.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_21.setText("")
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 380, 651, 81))
        self.groupBox_3.setStyleSheet("color: rgb(255, 85, 127);")
        self.groupBox_3.setObjectName("groupBox_3")
        self.lineEdit_22 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_22.setGeometry(QtCore.QRect(170, 20, 41, 20))
        self.lineEdit_22.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_22.setText("")
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.label_32 = QtWidgets.QLabel(self.groupBox_3)
        self.label_32.setGeometry(QtCore.QRect(10, 20, 161, 16))
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.groupBox_3)
        self.label_33.setGeometry(QtCore.QRect(10, 50, 151, 16))
        self.label_33.setObjectName("label_33")
        self.lineEdit_23 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_23.setGeometry(QtCore.QRect(170, 50, 41, 20))
        self.lineEdit_23.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_23.setText("")
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.lineEdit_24 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_24.setGeometry(QtCore.QRect(330, 20, 41, 20))
        self.lineEdit_24.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_24.setText("")
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.label_34 = QtWidgets.QLabel(self.groupBox_3)
        self.label_34.setGeometry(QtCore.QRect(220, 20, 111, 16))
        self.label_34.setObjectName("label_34")
        self.lineEdit_25 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_25.setGeometry(QtCore.QRect(330, 50, 41, 20))
        self.lineEdit_25.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_25.setText("")
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.label_35 = QtWidgets.QLabel(self.groupBox_3)
        self.label_35.setGeometry(QtCore.QRect(220, 50, 101, 16))
        self.label_35.setObjectName("label_35")
        self.lineEdit_26 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_26.setGeometry(QtCore.QRect(530, 20, 41, 20))
        self.lineEdit_26.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_26.setText("")
        self.lineEdit_26.setObjectName("lineEdit_26")
        self.label_36 = QtWidgets.QLabel(self.groupBox_3)
        self.label_36.setGeometry(QtCore.QRect(380, 20, 151, 16))
        self.label_36.setObjectName("label_36")
        self.lineEdit_27 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_27.setGeometry(QtCore.QRect(530, 50, 41, 20))
        self.lineEdit_27.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_27.setText("")
        self.lineEdit_27.setObjectName("lineEdit_27")
        self.label_37 = QtWidgets.QLabel(self.groupBox_3)
        self.label_37.setGeometry(QtCore.QRect(380, 50, 141, 16))
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.groupBox_3)
        self.label_38.setGeometry(QtCore.QRect(580, 20, 61, 16))
        self.label_38.setObjectName("label_38")
        self.lineEdit_28 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_28.setGeometry(QtCore.QRect(580, 40, 61, 31))
        self.lineEdit_28.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_28.setText("")
        self.lineEdit_28.setObjectName("lineEdit_28")
        self.label_34.raise_()
        self.label_32.raise_()
        self.lineEdit_22.raise_()
        self.label_33.raise_()
        self.lineEdit_23.raise_()
        self.lineEdit_24.raise_()
        self.lineEdit_25.raise_()
        self.label_35.raise_()
        self.lineEdit_26.raise_()
        self.label_36.raise_()
        self.lineEdit_27.raise_()
        self.label_37.raise_()
        self.label_38.raise_()
        self.lineEdit_28.raise_()
        self.groupBox_4 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 250, 651, 51))
        self.groupBox_4.setStyleSheet("color: rgb(255, 255, 0);")
        self.groupBox_4.setObjectName("groupBox_4")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_12.setGeometry(QtCore.QRect(100, 20, 61, 20))
        self.lineEdit_12.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.label_22 = QtWidgets.QLabel(self.groupBox_4)
        self.label_22.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label_22.setObjectName("label_22")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_13.setGeometry(QtCore.QRect(280, 20, 61, 20))
        self.lineEdit_13.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_13.setText("")
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.label_23 = QtWidgets.QLabel(self.groupBox_4)
        self.label_23.setGeometry(QtCore.QRect(170, 20, 111, 16))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.groupBox_4)
        self.label_24.setGeometry(QtCore.QRect(350, 20, 121, 16))
        self.label_24.setObjectName("label_24")
        self.lineEdit_14 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_14.setGeometry(QtCore.QRect(470, 20, 71, 20))
        self.lineEdit_14.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_14.setText("")
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.label_25 = QtWidgets.QLabel(self.groupBox_4)
        self.label_25.setGeometry(QtCore.QRect(550, 20, 31, 16))
        self.label_25.setObjectName("label_25")
        self.lineEdit_15 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_15.setGeometry(QtCore.QRect(590, 20, 41, 21))
        self.lineEdit_15.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.groupBox_5 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 460, 651, 81))
        self.groupBox_5.setStyleSheet("color: rgb(255, 85, 255);")
        self.groupBox_5.setObjectName("groupBox_5")
        self.lineEdit_29 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_29.setGeometry(QtCore.QRect(210, 20, 81, 20))
        self.lineEdit_29.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_29.setText("")
        self.lineEdit_29.setObjectName("lineEdit_29")
        self.label_39 = QtWidgets.QLabel(self.groupBox_5)
        self.label_39.setGeometry(QtCore.QRect(10, 20, 161, 16))
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.groupBox_5)
        self.label_40.setGeometry(QtCore.QRect(10, 50, 191, 16))
        self.label_40.setObjectName("label_40")
        self.lineEdit_30 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_30.setGeometry(QtCore.QRect(210, 50, 81, 20))
        self.lineEdit_30.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_30.setText("")
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.label_41 = QtWidgets.QLabel(self.groupBox_5)
        self.label_41.setGeometry(QtCore.QRect(300, 20, 131, 16))
        self.label_41.setObjectName("label_41")
        self.lineEdit_31 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_31.setGeometry(QtCore.QRect(430, 20, 101, 20))
        self.lineEdit_31.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_31.setText("")
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.lineEdit_32 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_32.setGeometry(QtCore.QRect(430, 50, 101, 20))
        self.lineEdit_32.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_32.setText("")
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.label_42 = QtWidgets.QLabel(self.groupBox_5)
        self.label_42.setGeometry(QtCore.QRect(300, 50, 121, 16))
        self.label_42.setObjectName("label_42")
        self.label_43 = QtWidgets.QLabel(self.groupBox_5)
        self.label_43.setGeometry(QtCore.QRect(540, 40, 31, 16))
        self.label_43.setObjectName("label_43")
        self.lineEdit_33 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_33.setGeometry(QtCore.QRect(590, 40, 41, 21))
        self.lineEdit_33.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_33.setObjectName("lineEdit_33")
        self.groupBox_7 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 540, 651, 141))
        self.groupBox_7.setStyleSheet("color: rgb(255, 255, 255);")
        self.groupBox_7.setObjectName("groupBox_7")
        self.lineEdit_34 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_34.setGeometry(QtCore.QRect(200, 20, 71, 20))
        self.lineEdit_34.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_34.setText("")
        self.lineEdit_34.setObjectName("lineEdit_34")
        self.label_44 = QtWidgets.QLabel(self.groupBox_7)
        self.label_44.setGeometry(QtCore.QRect(10, 20, 191, 16))
        self.label_44.setObjectName("label_44")
        self.lineEdit_35 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_35.setGeometry(QtCore.QRect(130, 50, 141, 20))
        self.lineEdit_35.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_35.setText("")
        self.lineEdit_35.setObjectName("lineEdit_35")
        self.label_45 = QtWidgets.QLabel(self.groupBox_7)
        self.label_45.setGeometry(QtCore.QRect(10, 50, 121, 16))
        self.label_45.setObjectName("label_45")
        self.lineEdit_36 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_36.setGeometry(QtCore.QRect(450, 20, 191, 20))
        self.lineEdit_36.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_36.setText("")
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.label_46 = QtWidgets.QLabel(self.groupBox_7)
        self.label_46.setGeometry(QtCore.QRect(280, 20, 161, 16))
        self.label_46.setObjectName("label_46")
        self.label_47 = QtWidgets.QLabel(self.groupBox_7)
        self.label_47.setGeometry(QtCore.QRect(280, 50, 191, 16))
        self.label_47.setObjectName("label_47")
        self.lineEdit_37 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_37.setGeometry(QtCore.QRect(470, 50, 171, 20))
        self.lineEdit_37.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_37.setText("")
        self.lineEdit_37.setObjectName("lineEdit_37")
        self.lineEdit_38 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_38.setGeometry(QtCore.QRect(140, 80, 181, 51))
        self.lineEdit_38.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_38.setText("")
        self.lineEdit_38.setObjectName("lineEdit_38")
        self.label_48 = QtWidgets.QLabel(self.groupBox_7)
        self.label_48.setGeometry(QtCore.QRect(10, 80, 131, 16))
        self.label_48.setObjectName("label_48")
        self.label_49 = QtWidgets.QLabel(self.groupBox_7)
        self.label_49.setGeometry(QtCore.QRect(330, 80, 131, 16))
        self.label_49.setObjectName("label_49")
        self.lineEdit_39 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_39.setGeometry(QtCore.QRect(460, 80, 181, 51))
        self.lineEdit_39.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_39.setText("")
        self.lineEdit_39.setObjectName("lineEdit_39")
        self.label_44.raise_()
        self.label_45.raise_()
        self.label_48.raise_()
        self.lineEdit_34.raise_()
        self.lineEdit_35.raise_()
        self.lineEdit_36.raise_()
        self.label_46.raise_()
        self.label_47.raise_()
        self.lineEdit_37.raise_()
        self.lineEdit_38.raise_()
        self.label_49.raise_()
        self.lineEdit_39.raise_()
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(200, 690, 251, 16))
        self.label_4.setObjectName("label_4")
        self.groupBox_6 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 90, 651, 80))
        self.groupBox_6.setStyleSheet("color: rgb(255, 170, 127);")
        self.groupBox_6.setObjectName("groupBox_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_6)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 51, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit.setGeometry(QtCore.QRect(80, 20, 171, 20))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit.setObjectName("lineEdit")
        self.label_8 = QtWidgets.QLabel(self.groupBox_6)
        self.label_8.setGeometry(QtCore.QRect(10, 50, 61, 16))
        self.label_8.setObjectName("label_8")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 50, 171, 20))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_9 = QtWidgets.QLabel(self.groupBox_6)
        self.label_9.setGeometry(QtCore.QRect(270, 20, 111, 16))
        self.label_9.setObjectName("label_9")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_3.setGeometry(QtCore.QRect(420, 20, 131, 20))
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_10 = QtWidgets.QLabel(self.groupBox_6)
        self.label_10.setGeometry(QtCore.QRect(270, 50, 151, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_4.setGeometry(QtCore.QRect(420, 50, 131, 20))
        self.lineEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_11 = QtWidgets.QLabel(self.groupBox_6)
        self.label_11.setGeometry(QtCore.QRect(560, 20, 31, 16))
        self.label_11.setObjectName("label_11")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_5.setGeometry(QtCore.QRect(600, 20, 41, 21))
        self.lineEdit_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 50, 81, 23))
        self.pushButton_2.setStyleSheet("background-color: rgb(170, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"font: 75 6pt \"MS Shell Dlg 2\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(10, 170, 651, 81))
        self.groupBox.setStyleSheet("color: rgb(255, 170, 0);")
        self.groupBox.setObjectName("groupBox")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_6.setGeometry(QtCore.QRect(90, 20, 21, 20))
        self.lineEdit_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(10, 20, 71, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(10, 50, 71, 16))
        self.label_13.setObjectName("label_13")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_7.setGeometry(QtCore.QRect(90, 50, 71, 20))
        self.lineEdit_7.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setGeometry(QtCore.QRect(180, 50, 121, 16))
        self.label_14.setObjectName("label_14")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_8.setGeometry(QtCore.QRect(310, 50, 71, 20))
        self.lineEdit_8.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(250, 20, 51, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_9.setGeometry(QtCore.QRect(310, 20, 71, 20))
        self.lineEdit_9.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        self.label_16.setGeometry(QtCore.QRect(120, 20, 121, 21))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setGeometry(QtCore.QRect(390, 50, 101, 16))
        self.label_17.setObjectName("label_17")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_10.setGeometry(QtCore.QRect(490, 50, 71, 20))
        self.lineEdit_10.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_11.setGeometry(QtCore.QRect(490, 20, 71, 20))
        self.lineEdit_11.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_11.setText("")
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.label_18 = QtWidgets.QLabel(self.groupBox)
        self.label_18.setGeometry(QtCore.QRect(390, 20, 91, 16))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.groupBox)
        self.label_19.setGeometry(QtCore.QRect(570, 20, 71, 51))
        self.label_19.setObjectName("label_19")
        self.groupBox_8 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_8.setGeometry(QtCore.QRect(10, 50, 651, 41))
        self.groupBox_8.setStyleSheet("color: rgb(255, 85, 0);")
        self.groupBox_8.setObjectName("groupBox_8")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_8)
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 41, 16))
        self.radioButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 8pt \"MS Shell Dlg 2\";")
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_8)
        self.radioButton_2.setGeometry(QtCore.QRect(60, 20, 51, 18))
        self.radioButton_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 8pt \"MS Shell Dlg 2\";")
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_8)
        self.radioButton_3.setGeometry(QtCore.QRect(120, 20, 61, 18))
        self.radioButton_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 8pt \"MS Shell Dlg 2\";")
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_8)
        self.radioButton_4.setGeometry(QtCore.QRect(180, 20, 71, 18))
        self.radioButton_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 8pt \"MS Shell Dlg 2\";")
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_8)
        self.radioButton_5.setGeometry(QtCore.QRect(260, 20, 71, 18))
        self.radioButton_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 8pt \"MS Shell Dlg 2\";")
        self.radioButton_5.setObjectName("radioButton_5")
        self.label_20 = QtWidgets.QLabel(self.groupBox_8)
        self.label_20.setGeometry(QtCore.QRect(340, 15, 71, 21))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.groupBox_8)
        self.label_21.setGeometry(QtCore.QRect(420, 13, 221, 21))
        self.label_21.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 255);\n"
"font: 75 9pt \"MS Shell Dlg 2\";")
        self.label_21.setObjectName("label_21")
        self.label_50 = QtWidgets.QLabel(self.frame)
        self.label_50.setGeometry(QtCore.QRect(510, 690, 47, 14))
        self.label_50.setObjectName("label_50")
        self.label_51 = QtWidgets.QLabel(self.frame)
        self.label_51.setGeometry(QtCore.QRect(560, 685, 91, 21))
        self.label_51.setStyleSheet("font: 75 8pt \"MS Shell Dlg 2\";\n"
"color: rgb(85, 170, 0);")
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.frame)
        self.label_52.setGeometry(QtCore.QRect(30, 689, 131, 16))
        self.label_52.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"font: 9pt \"Palatino Linotype\";")
        self.label_52.setObjectName("label_52")
        self.label_53 = QtWidgets.QLabel(self.frame)
        self.label_53.setGeometry(QtCore.QRect(270, 40, 401, 16))
        self.label_53.setStyleSheet("font: 6pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.label_53.setObjectName("label_53")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SATELLITE DATA DASHBOARD [V1.0]"))
        MainWindow.setWindowIcon(QtGui.QIcon(logo))
        self.pushButton.clicked.connect(self.get_serial_data_config)
        self.pushButton_2.clicked.connect(self.get_map_pos)
        self.label.setText(_translate("MainWindow", "COMPORT"))
        self.label_2.setText(_translate("MainWindow", "BAUDRATE"))
        self.label_3.setText(_translate("MainWindow", "🌎  GPS/GNSS/NavIC Dashboard 🛰️"))
        self.label_5.setText(_translate("MainWindow", "CHECKSUM:"))
        self.label_6.setText(_translate("MainWindow", "NO MATCH"))
        self.pushButton.setText(_translate("MainWindow", "🔒"))
        self.groupBox_2.setTitle(_translate("MainWindow", "GSA"))
        self.label_26.setText(_translate("MainWindow", "2D OR 3D FIX [A=AUTO; M=MANUAL]"))
        self.label_27.setText(_translate("MainWindow", "3D FIX [1=NO FIX; 2=2D FIX; 3= 3D FIX]"))
        self.label_28.setText(_translate("MainWindow", "PRN SATELLITES USED FOR FIX"))
        self.label_29.setText(_translate("MainWindow", "PDOP"))
        self.label_30.setText(_translate("MainWindow", "HDOP"))
        self.label_31.setText(_translate("MainWindow", "VDOP"))
        self.groupBox_3.setTitle(_translate("MainWindow", "GSV"))
        self.label_32.setText(_translate("MainWindow", "TOTAL NUMBER OF MESSAGES"))
        self.label_33.setText(_translate("MainWindow", "SATELLITE MESSAGE NUMBER"))
        self.label_34.setText(_translate("MainWindow", "SATELLITES IN VIEW"))
        self.label_35.setText(_translate("MainWindow", "SATELLITE PRN"))
        self.label_36.setText(_translate("MainWindow", "SATELLITE ELEVATION [DEG]"))
        self.label_37.setText(_translate("MainWindow", "SATELLITE AZIMUTH [DEG]"))
        self.label_38.setText(_translate("MainWindow", "SNR [C/No]"))
        self.groupBox_4.setTitle(_translate("MainWindow", "RMC"))
        self.label_22.setText(_translate("MainWindow", "SPEED [KNOTS]"))
        self.label_23.setText(_translate("MainWindow", "TRACK ANGLE [DEG]"))
        self.label_24.setText(_translate("MainWindow", "MAGNETIC VARIATION"))
        self.label_25.setText(_translate("MainWindow", "MODE"))
        self.groupBox_5.setTitle(_translate("MainWindow", "VTG"))
        self.label_39.setText(_translate("MainWindow", "TRUE TRACK MADE GOOD [DEG]"))
        self.label_40.setText(_translate("MainWindow", "MAGNETIC TRACK MADE GOOD [DEG]"))
        self.label_41.setText(_translate("MainWindow", "GROUND SPEED [KNOTS]"))
        self.label_42.setText(_translate("MainWindow", "GROUND SPEED [KM/H]"))
        self.label_43.setText(_translate("MainWindow", "MODE"))
        self.groupBox_7.setTitle(_translate("MainWindow", "NSF"))
        self.label_44.setText(_translate("MainWindow", "SATELLITE DATA RECEIVED FROM ID"))
        self.label_45.setText(_translate("MainWindow", "DATAFRAME RECEIVED"))
        self.label_46.setText(_translate("MainWindow", "MESSAGE FRAME RECEIVED: 55"))
        self.label_47.setText(_translate("MainWindow", "ALERT AND WARNING RECEIVED: 45"))
        self.label_48.setText(_translate("MainWindow", "DECODED MESSAGE[SF1]"))
        self.label_49.setText(_translate("MainWindow", "DECODED MESSAGE[SF2]"))
        self.label_4.setText(_translate("MainWindow", "© ALL RIGHTS RESERVED. -/ABHINABA [2022-23]"))
        self.groupBox_6.setTitle(_translate("MainWindow", "GLL"))
        self.label_7.setText(_translate("MainWindow", "LATITUDE"))
        self.label_8.setText(_translate("MainWindow", "LONGITUDE"))
        self.label_9.setText(_translate("MainWindow", "FIX TAKEN AT [UTC]"))
        self.label_10.setText(_translate("MainWindow", "STATUS (A=OK; V=NOT OK)"))
        self.label_11.setText(_translate("MainWindow", "MODE"))
        self.pushButton_2.setText(_translate("MainWindow", "📍LOCATE ON MAP"))
        self.groupBox.setTitle(_translate("MainWindow", "GGA"))
        self.label_12.setText(_translate("MainWindow", "FIX QUALITY "))
        self.label_13.setText(_translate("MainWindow", "SATELLITES"))
        self.label_14.setText(_translate("MainWindow", "HORIZONTAL DILUTION"))
        self.label_15.setText(_translate("MainWindow", "ALTITUDE"))
        self.label_16.setText(_translate("MainWindow", "-> [0=INVALID; 1-FIX]"))
        self.label_17.setText(_translate("MainWindow", "HEIGHT OF GEOID"))
        self.label_18.setText(_translate("MainWindow", "DGPS STATION ID"))
        self.label_19.setText(_translate("MainWindow", "UPDATE TIME"))
        self.groupBox_8.setTitle(_translate("MainWindow", "SELECT NAVIGATION SATELLITE TYPE"))
        self.radioButton.setText(_translate("MainWindow", "GPS"))
        self.radioButton_2.setText(_translate("MainWindow", "GNSS"))
        self.radioButton_3.setText(_translate("MainWindow", "NAVIC"))
        self.radioButton_4.setText(_translate("MainWindow", "GLONASS"))
        self.radioButton_5.setText(_translate("MainWindow", "BEIDOU"))
        self.label_20.setText(_translate("MainWindow", "🛰️ IN RANGE:"))
        self.label_21.setText(_translate("MainWindow", "1 3 5 7 9 11 14"))
        self.label_50.setText(_translate("MainWindow", "STATUS: "))
        self.label_51.setText(_translate("MainWindow", ""))
        self.label_52.setText(_translate("MainWindow", ""))
        self.label_53.setText(_translate("MainWindow", "❗PLEASE SELECT THE COMPORT , BAUDRATE AND SATELLITE TYPE AND PRESS LOCK BUTTON TO START."))
        self.label_21.setText("---")  # in range

    def get_serial_data_config(self):
        global com, baud
        com = self.comboBox.currentText()
        baud = self.comboBox_2.currentText()
        print(f"COMPORT: {com}  BAUDRATE: {baud}")
        self.label_51.setText("ONLINE 🛰️")
        self.main()

    def get_map_pos(self):
        global LAT, LONG
        from geopy.geocoders import Nominatim
        # Initialize Nominatim API
        geolocator = Nominatim(user_agent="geoapiExercises")
        # Assign Latitude & Longitude
        Latitude = LAT
        Latt = len(Latitude)
        Latitude = Latitude[:Latt - 1]
        Longitude = LONG
        Longg = len(Longitude)
        Longitude = Longitude[:Longg - 1]
        # Displaying Latitude and Longitude
        print("Latitude: ", Latitude)
        print("Longitude: ", Longitude)
        # Get location with geocode
        location = geolocator.geocode(Latitude + "," + Longitude)
        # Display location
        print("\nLocation of the given Latitude and Longitude:")
        print(location)
        self.messagebox.setIcon(QMessageBox.Information)
        self.messagebox.setText(location)
        self.messagebox.setWindowTitle("Global Address")
        self.messagebox.setStyleSheet("background-color : white")
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        QApplication.processEvents()
        self.messagebox.exec_()

    # Function to Get Lat & Long with UTC
    def getTime(self, string, format, returnFormat):
            return time.strftime(returnFormat,
                                 time.strptime(string, format))  # Convert date and time to a nice printable format

    def getLatLng(self, latString, lngString):
            lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:]) * 1.0 / 60.0).lstrip("0.")
            lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:]) * 1.0 / 60.0).lstrip("0.")
            return lat, lng

    ####################################################################

    # Frame Processors
    def printGLL(self, lines):
            global LAT, LONG
            print("========================================GIGLL========================================")
            lines = str(lines)
            format = lines.split(",")
            latlng = self.getLatLng(format[1], format[3])
            print("Lat,Long: ", latlng[0], format[2], ", ", latlng[1], format[4], sep='')
            LAT = str(latlng[0], format[2])
            LONG = str(latlng[1], format[4])
            self.lineEdit.setText(LAT)
            self.lineEdit_2.setText(LONG)
            print("Fix taken at:", self.getTime(format[5], "%H%M%S.%f", "%H:%M:%S"), "UTC")
            utc = (self.getTime(format[5], "%H%M%S.%f", "%H:%M:%S"))
            self.lineEdit_3.setText(utc)
            print("Status (A=OK,V=NOT OK):", format[6])
            self.lineEdit_4.setText(format[6])
            if format[7].partition("*")[0]:  # Extra field since NMEA standard 2.3
                    print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid, L= Looking):",
                          lines[7].partition("*")[0])
                    self.lineEdit_4.setText(lines[7].partition("*")[0])
            print("===================================GIGLL EOF========================================")
            return LAT, LONG

    def printGGA(self, lines):
            print("========================================GIGGA========================================")
            lines = str(lines)
            format = lines.split(",")
            print("Fix taken at:", self.getTime(format[1], "%H%M%S.%f", "%H:%M:%S"), "UTC")
            latlng = self.getLatLng(format[2], format[4])
            print("Lat,Long: ", latlng[0], format[3], ", ", latlng[1], format[5], sep='')
            print("Fix quality (0 = invalid, 1 = fix, 2..8):", lines[6])
            self.lineEdit_5.setText(lines[6])
            print("Satellites:", format[7].lstrip("0"))
            self.lineEdit_6.setText(format[7].lstrip("0"))
            print("Horizontal dilution:", format[8])
            self.lineEdit_7.setText(format[8])
            print("Altitude: ", format[9], format[10], sep="")
            alt = print(format[9], format[10], sep="")
            self.lineEdit_8.setText(alt)
            print("Height of geoid: ", format[11], format[12], sep="")
            geoid = print(format[11], format[12], sep="")
            self.lineEdit_9.setText(geoid)
            print("Time in seconds since last DGPS update:", format[13])
            self.label_19.setText(format[13])  # update
            print("DGPS station ID number:", format[14].partition("*")[0])
            self.lineEdit_9.setText(format[14].partition("*")[0])
            print("=====================================GIGGA EOF========================================")
            return

    def printRMC(self, lines):
            print("========================================GIRMC========================================")
            lines = str(lines)
            format = lines.split(",")
            print("Fix taken at:", self.getTime(format[1] + format[9], "%H%M%S.%f%d%m%y", "%a %b %d %H:%M:%S %Y"), "UTC")
            print("Status (A=OK,V=NOT OK):", format[2])
            latlng = self.getLatLng(format[3], format[5])
            print("Lat,Long: ", latlng[0], format[4], ", ", latlng[1], format[6], sep='')
            print("Speed (knots):", format[7])
            print("Track angle (deg):", format[8])
            print("Magnetic variation: ", format[10], end='')
            if len(format) == 13:  # The returned string will be either 12 or 13 - it will return 13 if NMEA standard used is above 2.3
                    print(format[11])
                    print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):",
                          format[12].partition("*")[0])
            else:
                    print(format[11].partition("*")[0])
            self.lineEdit_12.setText(format[7])  # speed
            self.lineEdit_13.setText(format[8])  # angle
            self.lineEdit_14.setText(format[10])  # magnetic
            self.lineEdit_15.setText(format[12].partition("*")[0])  # mode
            print("====================================GIRMC EOF========================================")
            return

    def printGSA(self, lines):
            print("========================================GIGSA========================================")
            lines = str(lines)
            format = lines.split(",")
            print("Selection of 2D or 3D fix (A=Auto,M=Manual):", format[1])
            print("3D fix (1=No fix,2=2D fix, 3=3D fix):", format[2])
            print("PRNs of satellites used for fix:", end='')
            for i in range(0, 12):
                    prn = format[3 + i].lstrip("0")
                    if prn:
                            print(" ", prn, end='')
            print("\nPDOP", format[15])
            print("\nHDOP", format[16])
            print("\nVDOP", format[17].partition("*")[0])
            self.lineEdit_16.setText("---")  # 2d
            self.lineEdit_17.setText("---")  # 3d
            self.lineEdit_18.setText("---")  # prn
            self.lineEdit_19.setText("---")  # pd
            self.lineEdit_20.setText("---")  # hd
            self.lineEdit_21.setText("---")  # vd
            print("====================================GIGSA EOF========================================")
            return

    def printGSV(self, lines):
            print("========================================GIGSV========================================")
            lines = str(lines)
            format = lines.split(",")
            print("Satellite total no of messages(1-9):", format[1])
            print("Satellite message number:", format[2])
            print("Satellites in view:", format[3])
            print("Satellite PRN:", format[4])
            print("Elevation (in deg):", format[5] + "°")
            print("Azimuth (deg):", format[6])
            print("SNR (C/No) 00-99dB:", format[7], "dB")
            self.lineEdit_22.setText("---")  # total
            self.lineEdit_23.setText("---")  # sat msg
            self.lineEdit_24.setText("---")  # view
            self.lineEdit_25.setText("---")  # prn
            self.lineEdit_26.setText("---")  # elevation
            self.lineEdit_27.setText("---")  # azimuth
            self.lineEdit_28.setText("---")  # srn
            print("====================================GIGSV EOF========================================")

    def printVTG(self, lines):
            print("========================================GIVTG========================================")
            lines = str(lines)
            format = lines.split(",")
            print("True Track made good (deg):", format[1], format[2])
            print("Magnetic track made good (deg):", format[3], format[4])
            print("Ground speed (knots):", format[5], format[6])
            print("Ground speed (km/h):", format[7], format[8].partition("*")[0])
            if lines[9].partition("*")[0]:  # Extra field since NMEA standard 2.3
                    print("Mode (A=Autonomous, D=Differential, E=Estimated, N=Data not valid):",
                          format[9].partition("*")[0])
            self.lineEdit_29.setText("---")  # true
            self.lineEdit_30.setText("---")  # mag
            self.lineEdit_31.setText("---")  # speed knot
            self.lineEdit_32.setText("---")  # speed kmph
            self.lineEdit_33.setText("---")  # mode
            print("=====================================GIVTG EOF========================================")
            return

    def printNSF(self, lines):
            print("========================================PIRNSF========================================")
            lines = str(lines)
            format = lines.split(",")
            print("Satellite data received from ID:", format[1], "STATUS : online")
            print("Dataframe received:", format[2])
            if format[8] == '55':
                    print("Message frame received: 55", format[3], format[4], format[5], format[6])
            else:
                    print("Alert and warning received: 45", format[3], format[4], format[5], format[6])
                    print(" Decode message from Subframe 1:", format[7], format[8], format[9], format[10], format[11],
                          format[12], format[13], format[14], format[15], format[16], format[17], format[18],
                          format[19],
                          format[20], format[21], format[22], format[23], format[24], format[25], format[26],
                          format[27],
                          format[28], format[29], format[30], format[31], format[32], format[33])
                    print("Decode messages from Subframe 2:", format[34], format[35], format[36], format[37],
                          format[38])
            self.lineEdit_34.setText("---")  # data rx
            self.lineEdit_35.setText("---")  # data frame
            self.lineEdit_36.setText("---")  # msg frame rx
            self.lineEdit_37.setText("---")  # alert
            self.lineEdit_38.setText("---")  # sf1
            self.lineEdit_39.setText("---")  # sf2
            print("=====================================PIRNSF EOF========================================")
            return

    # -----String decode---------#
    # Checksum
    def checksum(self, line):
            line = str(line)
            checkString = line.partition("*")
            checksum = 0
            for c in checkString[0]:
                    checksum ^= ord(c)
            try:
                    inputChecksum = int(checkString[2].rstrip(), 16)
            except:
                    print("Checksum Error Detected")
                    return False
            if checksum == inputChecksum:
                    print("===================================Checksum OK!===================================")
                    return True
            else:
                    print("=====================================================================================")
                    print("===================================Checksum error!===================================")
                    print("=====================================================================================")
                    print(hex(checksum), "!=", hex(inputChecksum))
                    return False

    # Main Code
    def main(self):
            global com, baud
            os.remove(logfile)
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)  # To indicate start of Program
            ser = serial.Serial(com, baud)
            capture_log()  # to log reading
            self.label_52.setText("LOGGING DATA.......")
            print("----Welcome to GPS/GNSS/GLONASS/NavIC Tracking System By @Abhinaba Ghosh [© 2022-23]----")
            while True:
                    reading = ser.readline()
                    # print(reading[0:6]) # to identify the format
                    # print(reading)
                    # self.checksum(reading)  # to check the checksum
                    if reading[0:6] == b"$GPGSV":
                            self.printGSV(reading)
                            # print(reading)
                    elif reading[0:6] == b"$GPGLL":
                            self.printGLL(reading)
                            # print(reading)
                    elif reading[0:6] == b"$GPGSA":
                            self.printGSA(reading)
                            # print(reading)
                    elif reading[0:6] == b"$GPRMC":
                            self.printRMC(reading)
                            # print(reading)
                    elif reading[0:6] == b"$GPGGA":
                            self.printGGA(reading)
                            # print(reading)
                    elif reading[0:6] == b"$GPVTG":
                            self.printVTG(reading)
                            # print(reading)
                    elif reading[0:6] == b"$PIRNSF":
                            self.printNSF(reading)
                            # print(reading)
                    else:
                            pass


# AUTO-LOG
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout

    def write(self, message):
        filename = logfile
        with open(filename, 'a', encoding='utf-8') as self.log:
            self.log.write(message)
        self.terminal.write(message)

    def flush(self):
        pass


def capture_log():
    Blue = "\033[94m{}\033[00m"
    print('[LOGGER]:', Blue.format('ACTIVE'))
    sys.stdout = Logger()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    splash = QSplashScreen()
    splash.setPixmap(QPixmap(splash_img).scaled(300, 250))
    splash.show()
    splash.showMessage('<h1 style="color:white;">Connecting to satellite.....</h1>',
                       Qt.AlignTop | Qt.AlignHCenter, Qt.green)
    time.sleep(5)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    splash.finish(MainWindow)
    sys.exit(app.exec_())
