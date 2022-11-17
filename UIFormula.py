from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QDialog, QPushButton, QLabel, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtCore
from PySide6.QtCore import QUrl
import requests
import ipaddress 


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.cam = QWebEngineView()
        self.iFormulaIP = ''

        self.btnLeft = QPushButton('left')
        self.btnLeft.clicked.connect(self.turnLeft)
        self.btnRight = QPushButton('Right')
        self.btnRight.clicked.connect(self.turnRight)
        self.btnForward = QPushButton('Forward')
        self.btnForward.clicked.connect(self.moveForward)
        self.btnBackward = QPushButton('Backward')
        self.btnBackward.clicked.connect(self.moveBackward)
        self.btnStop = QPushButton('Stop')
        self.btnStop.clicked.connect(self.stopMove)
        self.lblSpeed = QLabel("Speed")

        self.txtUrl = QLineEdit("i-Formula IP Address")
        self.btnLoad = QPushButton("Go")
        self.btnLoad.clicked.connect(self.load)
        self.lblName = QLabel("")
        self.lblStatus = QLabel("")

        # Create layout and add widgets
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.cam, 0, 0, 4, 8)
        self.mainLayout.addWidget(self.txtUrl, 4, 0, 1, 4)
        self.mainLayout.addWidget(self.btnLoad, 4, 5, 1, 1)
        self.mainLayout.addWidget(self.lblName, 4, 6, 1, 2)
        self.mainLayout.addWidget(self.btnLeft, 5, 0, 3, 2)
        self.mainLayout.addWidget(self.btnForward, 5, 2, 1, 2)
        self.mainLayout.addWidget(self.btnStop, 6, 2, 1, 2)
        self.mainLayout.addWidget(self.btnBackward, 7, 2, 1, 2)
        self.mainLayout.addWidget(self.btnRight, 5, 4, 3, 2)
        self.mainLayout.addWidget(self.lblSpeed,5, 6, 1, 2)
        self.mainLayout.addWidget(self.lblStatus, 8, 0, 1, 8)

        self.setLayout(self.mainLayout)
        self.lblStatus.setText('Ready')

    @QtCore.Slot()
    def load(self):
    	self.lblStatus.setText(f'Connecting to i-Formula...')
    	try:
    	    ip = ipaddress.ip_address(self.txtUrl.text())
    	    print(f'IP address {self.txtUrl.text()} is valid. The object returned is {ip}')
    	    response = requests.get(f'http://{self.txtUrl.text()}:12321/')
    	    self.lblName.setText(f'{response.text}')
    	    self.iFormulaIP = self.txtUrl.text()
    	    self.cam.load(QUrl(f'http://{self.iFormulaIP}:12321/camlive'))
    	    self.lblStatus.setText(f'i-Formula connected')
    	    print('i-Formula Cam live now~')

    	except ValueError:
            self.lblStatus.setText(f'IP address {self.txtUrl.text()} is not valid')
            print(f'IP address {self.txtUrl.text()} is not valid')

    @QtCore.Slot()
    def turnLeft(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=2")
        print(f'{response.status_code}: {response.text}')

    @QtCore.Slot()
    def turnRight(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=3")
        print(f'{response.status_code}: {response.text}')

    @QtCore.Slot()
    def moveForward(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=1")
        print(f'{response.status_code}: {response.text}')

    @QtCore.Slot()
    def stopMove(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls")
        print(f'{response.status_code}: {response.text}')

    @QtCore.Slot()
    def moveBackward(self):
        response = requests.get(f"https://{self.iFormulaIP}:12321/controls?c=4")
        print(f'{response.status_code}: {response.text}')

