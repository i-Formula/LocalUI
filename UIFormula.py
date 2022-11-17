from ctypes import alignment
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QDialog, QPushButton, QLabel, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtCore
from PySide6.QtCore import QUrl
import requests


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.cam = QWebEngineView()        
        #self.cam.setLayout(720, 480)
        self.iFormulaIP = ''
    
        #self.setCentralWidget(self.webEngineView)                
        #self.webEngineView.page().urlChanged.connect(self.urlChanged)
        self.btnLeft = QPushButton('left')
        self.btnLeft.clicked.connect(self.turnLeft)
        self.btnRight = QPushButton('Right')
        self.btnRight.clicked.connect(self.turnRight)
        self.btnForward = QPushButton('Forward')
        self.btnForward.clicked.connect(self.moveForward)
        self.btnBackward = QPushButton('Backward')
        #self.btnBackward.clicked.connect(self.)
        self.btnStop = QPushButton('Stop')
        self.btnStop.clicked.connect(self.stopMove)
        self.lblSpeed = QLabel("Speed")

        self.txtUrl = QLineEdit("i-Formula IP Address")
        self.btnLoad = QPushButton("Go")
        self.btnLoad.clicked.connect(self.load)
        self.lblName = QLabel("")

        # Create layout and add widgets
        self.moveLayout = QVBoxLayout()
        self.moveLayout.addWidget(self.btnForward)
        self.moveLayout.addWidget(self.btnStop)
        self.moveLayout.addWidget(self.btnBackward)

        self.controlLayout = QHBoxLayout()
        self.controlLayout.addWidget(self.btnLeft)
        self.controlLayout.addLayout(self.moveLayout)
        self.controlLayout.addWidget(self.btnRight)
        self.controlLayout.addWidget(self.lblSpeed)
        
        self.connection = QHBoxLayout()
        self.connection.addWidget(self.txtUrl)
        self.connection.addWidget(self.btnLoad)
        self.connection.addWidget(self.lblName)

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
        #self.mainLayout.addLayout(self.connection,1,0,1,1)
        #self.mainLayout.addLayout(self.controlLayout,2,0,2,1)
        # Set dialog layout
        self.setLayout(self.mainLayout)
        #self.cam.load('http://172.18.8.83:12321/camlive')

    @QtCore.Slot()
    def load(self):
        self.iFormulaIP = self.txtUrl.text()
        self.cam.load(QUrl(f'http://{self.iFormulaIP}:12321/camlive'))
        #self.cam.page().urlChanged.connect(self.urlChanged)

    @QtCore.Slot()
    def turnLeft(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=2")
        print(response)

    @QtCore.Slot()
    def turnRight(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=3")
        print(response)

    @QtCore.Slot()
    def moveForward(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=1")
        print(response)

    @QtCore.Slot()
    def stopMove(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls")
        print(response)

