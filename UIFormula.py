from PySide6.QtWidgets import QComboBox, QGridLayout, QDialog, QPushButton, QLabel, QLineEdit, QVBoxLayout, QRadioButton, QButtonGroup, QCheckBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtCore
from PySide6.QtCore import QUrl
import requests, ipaddress, time, json, zipfile, os
from io import BytesIO
from AITraining import AITraining


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.cam = QWebEngineView()
        self.cam.setZoomFactor(2.0)
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
        self.cbxSpeed.addItems(['0', '4', '5'])
        self.cbxSpeed.currentTextChanged.connect(self.onSpeedChanged)
        self.btnAuto = QPushButton('Autopilot')
        self.btnAuto.setDisabled(True)

        # Status
        self.lblLog = QLabel('')
        self.lblLog.wordWrap = True

        #network connection widget
        self.txtUrl = QLineEdit()
        self.txtUrl.setPlaceholderText('Enter IP Address')
        self.btnLoad = QPushButton('Connect')
        self.btnLoad.clicked.connect(self.load)
        self.lblName = QLabel('')
        #self.btnUnLoad = QPushButton('Disconnect')

        # AI Training Widget
        self.chkTrain = QCheckBox('Sampling Mode')
        self.chkTrain.clicked.connect(self.sample)
        self.sampling = self.chkTrain.isChecked()
        self.radFree = QRadioButton('Free')
        self.radLeft = QRadioButton('Left')
        self.radRight= QRadioButton('Right')
        self.radBlock= QRadioButton('Block')
        self.radBlock.setDisabled(True)
        self.radFree.setDisabled(True)
        self.radRight.setDisabled(True)
        self.radLeft.setDisabled(True)
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
        self.btnTakeShot.setDisabled(True)
        self.btnSTrainingRemote = QPushButton('Training on the car')
        self.btnSTrainingRemote.clicked.connect(self.training)
        self.btnSTrainingRemote.setDisabled(True)
        self.btnSTrainingLocal = QPushButton('Download and Train')
        self.btnSTrainingLocal.clicked.connect(self.localTraining)
        #self.btnSTrainingLocal.setDisabled(True)

        # Create layout and add widgets
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.cam, 0, 0, 10, 10)
        self.mainLayout.addWidget(self.txtUrl, 10, 0, 1, 3)
        self.mainLayout.addWidget(self.btnLoad, 10, 3, 1, 1)
        self.mainLayout.addWidget(self.lblName, 10, 4, 1, 2)
        #self.mainLayout.addWidget(self.btnUnLoad, 10, 6, 1, 1)
        self.mainLayout.addWidget(self.lblLog, 11, 0, 4, 3)

        self.mainLayout.addWidget(self.btnLeft, 12, 4, 1, 1)
        self.mainLayout.addWidget(self.btnForward, 11, 5, 1, 1)
        self.mainLayout.addWidget(self.btnStop, 12, 5, 1, 1)
        self.mainLayout.addWidget(self.btnBackward, 13, 5, 1, 1)
        self.mainLayout.addWidget(self.btnRight, 12, 6, 1, 1)
        
        self.mainLayout.addWidget(self.lblSpeed, 14, 4, 1, 1)
        self.mainLayout.addWidget(self.cbxSpeed, 14, 5, 1, 1)
        #self.mainLayout.addWidget(self.btnAuto, 14, 6, 1, 1)
        self.mainLayout.addWidget(self.btnAuto, 10, 6, 1, 1)
        self.mainLayout.addWidget(self.chkTrain, 14, 6, 1, 1)

        self.mainLayout.addLayout(self.groupAI, 12, 8, 3, 1)
        self.mainLayout.addWidget(self.btnTakeShot, 12, 9, 1, 1)
        self.mainLayout.addWidget(self.btnSTrainingRemote, 13, 9, 1, 1)
        self.mainLayout.addWidget(self.btnSTrainingLocal, 14, 9, 1, 1)

        self.setLayout(self.mainLayout)
        self.lblLog.setText('Ready')

    def sampleCount(self):
        response = requests.get(f'http://{self.txtUrl.text()}:12321/samples')
        jsonValue = response.json()
        for r in jsonValue:
            self.lblLog.setText(f'{self.lblLog.text()}\n{r}: {jsonValue[r]}')

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
            self.lblLog.setText(f'{self.lblLog.text()}i-Formula connected\n')
            print('i-Formula Cam live now~')
        except ValueError:
            self.lblLog.setText(f'{self.lblLog.text()}IP address {self.txtUrl.text()} is not valid')
            print(f'IP address {self.txtUrl.text()} is not valid')
        
        self.sampleCount()

    @QtCore.Slot()
    def turnLeft(self): #2
        if self.sampling:
            print('capture left sample')
            requests.get(f"http://{self.iFormulaIP}:12321/takesnap?i=2")
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=2")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')
        self.sampleCount()

    @QtCore.Slot()
    def turnRight(self): #3
        if self.sampling:
            print('capture right sample')
            requests.get(f"http://{self.iFormulaIP}:12321/takesnap?i=3")
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=3")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')
        self.sampleCount()

    @QtCore.Slot()
    def moveForward(self): #1
        print(self.sampling)
        response =''
        if self.sampling:
            print('capture free sample')
            requests.get(f"http://{self.iFormulaIP}:12321/takesnap?i=1")
            response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=1")
            print(f'{response.status_code}: {response.text}')
            time.sleep(0.1)
            response = requests.get(f"http://{self.iFormulaIP}:12321/controls")
            print(f'{response.status_code}: {response.text}')
        else:
            response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=1")
            print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')
        self.sampleCount()

    @QtCore.Slot()
    def stopMove(self): 
        response = requests.get(f"http://{self.iFormulaIP}:12321/controls")
        print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')
        self.sampleCount()

    @QtCore.Slot()
    def moveBackward(self): #4
        response = ''
        if self.sampling:
            print('capture block sample')
            response = requests.get(f"http://{self.iFormulaIP}:12321/takesnap?i=4")
            print(f'{response.status_code}: {response.text}')
            
            response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=4")
            print(f'{response.status_code}: {response.text}')
            time.sleep(0.1)
            response = requests.get(f"http://{self.iFormulaIP}:12321/controls")
            print(f'{response.status_code}: {response.text}')
        else: 
            response = requests.get(f"http://{self.iFormulaIP}:12321/controls?c=4")
            print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'({response.status_code}): {response.text} ')
        self.sampleCount()

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
    def localTraining(self):
        self.lblLog.setText(f'Preparing to download the files\n')
        response = requests.get(f"http://{self.iFormulaIP}:12321/download")
        z= zipfile.ZipFile(BytesIO(response.content))
        z.extractall(os.getcwd())

        #print(f'{response.status_code}: {response.text}')
        self.lblLog.setText(f'Samples download completed.  Start training...\n')
        # Road to AI Training
        t = AITraining()
        t.training()
        self.lblLog.setText(f'Training completed.  Now uploading...\n')
        # Upload model
        print(f'Uploading model...')
        response = requests.post(f"http://{self.iFormulaIP}:12321/upload", files={'model': open('best_steering_model_xy.pth', 'rb')})
        self.lblLog.setText(f'[{response.status_code}: upload completed]\n')
        print('Model upload completed...')

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

    @QtCore.Slot()
    def sample(self):
        self.sampling = self.chkTrain.isChecked()