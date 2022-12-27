# -*- coding: utf-8 -*-
import os
import sys
import glob
import serial
import psutil
import socket
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
global result, value, gyro

val = None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(777, 521)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 200, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 200, 61, 16))
        self.label_2.setObjectName("label_2")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(250, 220, 71, 31))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(350, 220, 71, 31))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(667, 50, 101, 23))
        self.battery_status()
        self.progressBar.setProperty("value", value)
        self.progressBar.setObjectName("progressBar")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(560, 60, 91, 16))
        self.label_3.setObjectName("label_3")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(230, 70, 221, 121))
        self.listView.setObjectName("listView")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 91, 31))
        self.comboBox.setObjectName("comboBox")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(110, 40, 81, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(570, 300, 101, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(570, 400, 101, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(470, 350, 101, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(670, 350, 101, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.listView_2 = QtWidgets.QListView(self.centralwidget)
        self.listView_2.setGeometry(QtCore.QRect(580, 360, 81, 31))
        self.listView_2.setObjectName("listView_2")
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(20, 310, 71, 151))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.verticalSlider.valueChanged.connect(self.update_speed)  # Throttle speed value
        self.gyro_stabilization()
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(100, 360, 101, 61))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setProperty("value", gyro)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(550, 100, 47, 13))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(550, 140, 61, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(590, 180, 47, 13))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(550, 260, 101, 20))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(590, 220, 47, 13))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(40, 280, 51, 31))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 300, 21, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(10, 430, 21, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(10, 370, 41, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(120, 340, 61, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(90, 420, 16, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(190, 420, 16, 20))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(140, 420, 16, 16))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(230, 50, 81, 21))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(160, 90, 71, 16))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(110, 130, 111, 16))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(110, 170, 101, 16))
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(110, 250, 47, 13))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(270, 280, 141, 16))
        self.label_23.setObjectName("label_23")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(480, 420, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(690, 420, 75, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.listView_3 = QtWidgets.QListView(self.centralwidget)
        self.listView_3.setGeometry(QtCore.QRect(210, 300, 251, 171))
        self.listView_3.setObjectName("listView_3")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(460, 210, 75, 23))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(460, 250, 75, 23))
        self.pushButton_8.setObjectName("pushButton_8")
        self.listView_4 = QtWidgets.QListView(self.centralwidget)
        self.listView_4.setGeometry(QtCore.QRect(670, 250, 91, 31))
        self.listView_4.setObjectName("listView_4")

        model = QtGui.QStandardItemModel()      # to update values in listview
        self.listView_4.setModel(model)
        if val == None:
            data = 'No data'
            item = QtGui.QStandardItem(data)
            model.appendRow(item)
        else:
            item = QtGui.QStandardItem(val)
            model.appendRow(item)

        self.listView_5 = QtWidgets.QListView(self.centralwidget)
        self.listView_5.setGeometry(QtCore.QRect(670, 210, 91, 31))
        self.listView_5.setObjectName("listView_5")
        self.listView_6 = QtWidgets.QListView(self.centralwidget)
        self.listView_6.setGeometry(QtCore.QRect(670, 170, 91, 31))
        self.listView_6.setObjectName("listView_6")
        self.listView_7 = QtWidgets.QListView(self.centralwidget)
        self.listView_7.setGeometry(QtCore.QRect(610, 130, 151, 31))
        self.listView_7.setObjectName("listView_7")
        self.listView_8 = QtWidgets.QListView(self.centralwidget)
        self.listView_8.setGeometry(QtCore.QRect(610, 90, 151, 31))
        self.listView_8.setObjectName("listView_8")
        self.listView_9 = QtWidgets.QListView(self.centralwidget)
        self.listView_9.setGeometry(QtCore.QRect(10, 240, 91, 31))
        self.listView_9.setObjectName("listView_9")
        self.listView_10 = QtWidgets.QListView(self.centralwidget)
        self.listView_10.setGeometry(QtCore.QRect(10, 200, 91, 31))
        self.listView_10.setObjectName("listView_10")
        self.listView_11 = QtWidgets.QListView(self.centralwidget)
        self.listView_11.setGeometry(QtCore.QRect(10, 160, 91, 31))
        self.listView_11.setObjectName("listView_11")
        self.listView_12 = QtWidgets.QListView(self.centralwidget)
        self.listView_12.setGeometry(QtCore.QRect(10, 120, 91, 31))
        self.listView_12.setObjectName("listView_12")
        self.listView_13 = QtWidgets.QListView(self.centralwidget)
        self.listView_13.setGeometry(QtCore.QRect(10, 80, 141, 31))
        self.listView_13.setObjectName("listView_13")
        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        self.label_27.setGeometry(QtCore.QRect(110, 210, 121, 16))
        self.label_27.setObjectName("label_27")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(250, 260, 31, 23))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(350, 260, 31, 23))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(290, 260, 31, 23))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_13.setGeometry(QtCore.QRect(390, 260, 31, 23))
        self.pushButton_13.setObjectName("pushButton_13")
        self.label_28 = QtWidgets.QLabel(self.centralwidget)
        self.label_28.setGeometry(QtCore.QRect(260, 20, 171, 31))
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        self.label_29.setGeometry(QtCore.QRect(570, 460, 111, 20))
        self.label_29.setObjectName("label_29")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(464, 90, 61, 71))
        self.pushButton_11.setObjectName("pushButton_11")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 777, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WIRELESS REMOTE CONTROLLER"))
        self.label.setText(_translate("MainWindow", "SET ALTITUDE"))
        self.label_2.setText(_translate("MainWindow", "SET SPEED"))
        self.label_3.setText(_translate("MainWindow", "FLIGHT POWER"))
        self.serial_ports()
        self.comboBox.addItems(result)
        self.comboBox.currentTextChanged.connect(self.text_changed)
        self.label_4.setText(_translate("MainWindow", "COMPORT"))
        self.pushButton.setText(_translate("MainWindow", "FORWARD"))
        self.pushButton_2.setText(_translate("MainWindow", "BACKWARD"))
        self.pushButton_3.setText(_translate("MainWindow", "STEER LEFT"))
        self.pushButton_4.setText(_translate("MainWindow", "STEER RIGHT"))
        self.label_5.setText(_translate("MainWindow", "LATITUDE"))
        self.label_6.setText(_translate("MainWindow", "LONGITUDE"))
        self.label_7.setText(_translate("MainWindow", "W_SPEED"))
        self.label_8.setText(_translate("MainWindow", "SATELLITES VIEWED"))
        self.label_9.setText(_translate("MainWindow", "ALTITUDE"))
        self.label_10.setText(_translate("MainWindow", "THROTTLE"))
        self.label_11.setText(_translate("MainWindow", "MAX"))
        self.label_12.setText(_translate("MainWindow", "MIN"))
        self.label_13.setText(_translate("MainWindow", "AVG----"))
        self.label_14.setText(_translate("MainWindow", "G-STABILIZER"))
        self.label_15.setText(_translate("MainWindow", "L"))
        self.label_16.setText(_translate("MainWindow", "R"))
        self.label_17.setText(_translate("MainWindow", "S"))
        self.label_18.setText(_translate("MainWindow", "TERMINAL"))
        self.label_19.setText(_translate("MainWindow", "REMOTE IP"))
        self.label_20.setText(_translate("MainWindow", "SYSTEM TEMPERATURE"))
        self.label_21.setText(_translate("MainWindow", "AMBIENT HUMIDITY"))
        self.label_22.setText(_translate("MainWindow", "ALERT"))
        self.label_23.setText(_translate("MainWindow", "REALTIME CAMERA FEED"))
        self.pushButton_5.setText(_translate("MainWindow", "PITCH"))
        self.pushButton_6.setText(_translate("MainWindow", "ROLL"))
        self.pushButton_7.setText(_translate("MainWindow", "TAKE-OFF"))
        self.pushButton_8.setText(_translate("MainWindow", "LAND"))
        self.label_27.setText(_translate("MainWindow", "AMBIENT TEMPERATURE"))
        self.pushButton_9.setText(_translate("MainWindow", "-"))
        self.pushButton_10.setText(_translate("MainWindow", "-"))
        self.pushButton_12.setText(_translate("MainWindow", "+"))
        self.pushButton_13.setText(_translate("MainWindow", "+"))
        self.label_28.setText(_translate("MainWindow", "WIRELESS FLIGHT CONTROLLER"))
        self.label_29.setText(_translate("MainWindow", "STEERING CONTROLS"))
        self.pushButton_11.setText(_translate("MainWindow", "RESET"))

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        global result
        result = []
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def text_changed(self, s):
        print("Selected ComPort:", s)
        return s

    def battery_status(self):
        global value
        value = 39
        return value

    def gyro_stabilization(self):
        global gyro
        gyro = 56
        print("GYRO stabilization: ", gyro)
        return gyro

    def update_speed(self, event):
        print(event)
        self.lcdNumber_2.display(event)

    def gps_data(self):
        lat = ""
        long = ""
        azimuth = ""
        altitude = ""
        satellites = ""
        pass

    def onboard_temperature(self):
        pass

    def dht22_data(self):
        pass

    def terminal_view(self):
        pass

    def camera_feed(self):
        pass

    def get_altitude_data(self):
        pass

    def get_flight_module_ip(self):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
