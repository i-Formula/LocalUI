from PySide6.QtWidgets import QComboBox, QGridLayout, QDialog, QPushButton, QLabel, QLineEdit, QVBoxLayout, QRadioButton, QButtonGroup
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

        # control widget
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

        # Speed controls
        self.lblSpeed = QLabel('Speed')
        self.cbxSpeed = QComboBox(self)
        self.cbxSpeed.addItems(['1', '2', '3', '4', '5'])
        self.cbxSpeed.currentTextChanged.connect(self.onSpeedChanged)
        self.btnAuto = QPushButton('Autopilot')

        # Status
        self.lblLog = QLabel('')
        self.lblLog.wordWrap = True

        #network connection widget
        self.txtUrl = QLineEdit()
        self.txtUrl.setPlaceholderText('Enter IP Address')
        self.btnLoad = QPushButton('Connect')
        self.btnLoad.clicked.connect(self.load)
        self.lblName = QLabel('')
        self.btnUnLoad = QPushButton('Disconnect')

        # AI Training Widget
        self.radFree = QRadioButton('Free')
        self.radLeft = QRadioButton('Left')
        self.radRight= QRadioButton('Right')
        self.radBlock= QRadioButton('Block')
        self.groupAI = QVBoxLayout()
        self.groupAI.addWidget(self.radFree)
        self.groupAI.addWidget(self.radLeft)
        self.groupAI.addWidget(self.radRight)
        self.groupAI.addWidget(self.radBlock)
        self.buttongroup1 = QButtonGroup(self)
        self.buttongroup1.addButton(self.radFree, 1)
        self.buttongroup1.addButton(self.radLeft, 2)
        self.buttongroup1.addButton(self.radRight, 3)
        self.buttongroup1.addButton(self.radBlock, 4)
        self.buttongroup1.buttonClicked.connect(self.slapshot)
        self.btnTakeShot = QPushButton('Take a Shot')
        self.btnTakeShot.clicked.connect(self.slapshot)
        self.btnSTrainingRemote = QPushButton('Remote Training')
        self.btnSTrainingRemote.clicked.connect(self.training)
        self.btnSTrainingLocal = QPushButton('Local Training')

        # Create layout and add widgets
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.cam, 0, 0, 10, 10)
        self.mainLayout.addWidget(self.txtUrl, 10, 0, 1, 3)
        self.mainLayout.addWidget(self.btnLoad, 10, 3, 1, 1)
        self.mainLayout.addWidget(self.lblName, 10, 4, 1, 2)
        self.mainLayout.addWidget(self.btnUnLoad, 10, 6, 1, 1)
        self.mainLayout.addWidget(self.lblLog, 11, 0, 4, 3)

        self.mainLayout.addWidget(self.btnLeft, 12, 4, 1, 1)
        self.mainLayout.addWidget(self.btnForward, 11, 5, 1, 1)
        self.mainLayout.addWidget(self.btnStop, 12, 5, 1, 1)
        self.mainLayout.addWidget(self.btnBackward, 13, 5, 1, 1)
        self.mainLayout.addWidget(self.btnRight, 12, 6, 1, 1)
        
        self.mainLayout.addWidget(self.lblSpeed, 14, 4, 1, 1)
        self.mainLayout.addWidget(self.cbxSpeed, 14, 5, 1, 1)
        self.mainLayout.addWidget(self.btnAuto, 14, 6, 1, 1)

        self.mainLayout.addLayout(self.groupAI, 12, 8, 3, 1)
        self.mainLayout.addWidget(self.btnTakeShot, 12, 9, 1, 1)
        self.mainLayout.addWidget(self.btnSTrainingRemote, 13, 9, 1, 1)
        self.mainLayout.addWidget(self.btnSTrainingLocal, 14, 9, 1, 1)

        self.setLayout(self.mainLayout)
        self.lblLog.setText('Ready')

    @QtCore.Slot()
    def load(self):
    	self.lblLog.setText(f'Connecting to i-Formula...\n')
    	try:
    	    ip = ipaddress.ip_address(self.txtUrl.text())
    	    print(f'IP address {self.txtUrl.text()} is valid. The object returned is {ip}')
    	    response = requests.get(f'http://{self.txtUrl.text()}:12321/')
    	    self.lblName.setText(f'{response.text}\n')
    	    self.iFormulaIP = self.txtUrl.text()
    	    self.cam.load(QUrl(f'http://{self.iFormulaIP}:12321/camlive'))
    	    self.lblLog.setText(f'{self.lblLog.text()}i-Formula connected')
    	    print('i-Formula Cam live now~')

    	except ValueError:
            self.lblLog.setText(f'{self.lblLog.text()}IP address {self.txtUrl.text()} is not valid')
            print(f'IP address {self.txtUrl.text()} is not valid')

    @QtCore.Slot()
    def turnLeft(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=2")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')

    @QtCore.Slot()
    def turnRight(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=3")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')

    @QtCore.Slot()
    def moveForward(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=1")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')

    @QtCore.Slot()
    def stopMove(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')

    @QtCore.Slot()
    def moveBackward(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=4")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')

    @QtCore.Slot()
    def onSpeedChanged(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/speed?c={self.cbxSpeed.currentText()}")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')

    @QtCore.Slot()
    def training(self):
        response = requests.get(f"http://{self.iFormulaIP}:12321/train")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')

    @QtCore.Slot()
    def slapshot(self):
        if self.buttongroup1.checkedId()==1:
            print('1 checked')
            response = requests.get(f"http://{self.iFormulaIP}:12321/takesnap?i=1")
        elif self.buttongroup1.checkedId()==2:
            print('2 checked')
            response = requests.get(f"http://{self.iFormulaIP}:12321/takesnap?i=2")
        elif self.buttongroup1.checkedId()==3:
            print('3 checked')
            response = requests.get(f"http://{self.iFormulaIP}:12321/takesnap?i=3")
        elif self.buttongroup1.checkedId()==4:
            print('4 checked')
            response = requests.get(f"http://{self.iFormulaIP}:12321/takesnap?i=4")     
        else:
            print('? checked')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')
