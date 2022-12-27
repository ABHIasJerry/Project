from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700, 350)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.counter = 0
        self.n = 100
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)
    def initUI(self):
        # layout to display splash scrren frame
        layout = QVBoxLayout()
        self.setLayout(layout)
        # splash screen frame
        self.frame = QFrame()
        layout.addWidget(self.frame)
        # splash screen title
        self.title_label = QLabel(self.frame)
        self.title_label.setObjectName('title_label')
        self.title_label.resize(690, 120)
        self.title_label.move(0, 5) # x, y
        self.title_label.setText('FLIGHT CONTROL DESK')
        self.title_label.setAlignment(Qt.AlignCenter)
        # splash screen title description
        self.description_label = QLabel(self.frame)
        self.description_label.resize(690, 40)
        self.description_label.move(0, self.title_label.height())
        self.description_label.setObjectName('desc_label')
        self.description_label.setText('<b>@Copyright, 2022 | Abhinaba </b>')
        self.description_label.setAlignment(Qt.AlignCenter)
        # splash screen pogressbar
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, 180) # self.description_label.y()+130
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)
        # spash screen loading label
        self.loading_label = QLabel(self.frame)
        self.loading_label.resize(self.width() - 10, 50)
        self.loading_label.move(0, self.progressBar.y() + 70)
        self.loading_label.setObjectName('loading_label')
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setText('Loading...')
    def loading(self):
        # set progressbar value
        self.progressBar.setValue(self.counter)
        # stop progress if counter
        # is greater than n and
        # display main window app
        if self.counter >= self.n:
            self.timer.stop()
            self.close()
            time.sleep(1)
            self.WindowApp = WindowApp()
            self.WindowApp.show()
        self.counter += 1
class WindowApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(400, 200, 320, 315)
        self.show()
app = QApplication(sys.argv)
app.setStyleSheet('''
        #title_label {
            font-size: 50px;
            color: #ffffff;
        }
        #desc_label {
            font-size: 20px;
            color: #c2ced1;
        }
        #loading_label {
            font-size: 30px;
            color: #e8e8eb;
        }
        QFrame {
            background-color: #625899;
            color: #c8c8c8;
        }
        QProgressBar {
            background-color: #000000;
            color: #c8c8c8;
            border-style: none;
            border-radius: 5px;
            text-align: center;
            font-size: 25px;
        }
        QProgressBar::chunk {
            border-radius: 5px;
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #44DD44);
        }
''')
splash = SplashScreen()
splash.show()
sys.exit(app.exec_())