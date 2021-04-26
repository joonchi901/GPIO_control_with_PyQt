import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


class PbarThread(QThread):
    change_value = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.cnt = 0
        self.a = 1

    def run(self):
        while self.a:
            if self.cnt == 100:
                self.cnt = -1
            self.cnt += 1
            self.change_value.emit(self.cnt)
            self.msleep(300)

class TimerThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.tm = 6
        self.b = 1

    def run(self):
        while self.b:
            print(str(self.tm))
            self.tm -= 1
            self.msleep(1000)

class SensorThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.tm = 10
        self.b = 1

    def run(self):
        while self.b:
            print(str(self.tm))
            self.tm -= 1
            self.msleep(1000)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.createRadioButtonGroup())
        grid.addWidget(self.createProgressBarGroup())
        grid.addWidget(self.createTextLabelGroup())
        grid.addWidget(self.createComboBoxGroup())
        self.ss = SensorThread()
        self.ss.start()
        self.setLayout(grid)

        self.setWindowTitle('철도 교통제어 GUI')
        self.setGeometry(300, 300, 350, 220)
        self.show()

    def createRadioButtonGroup(self):
        groupbox = QGroupBox('운행 상태')

        self.rbtn1 = QRadioButton('진입 대기', self)
        self.rbtn1.setDisabled(True)
        self.rbtn1.setChecked(True)
        self.rbtn2 = QRadioButton('진입 중', self)
        self.rbtn2.setDisabled(True)
        self.rbtn3 = QRadioButton('운행 대기', self)
        self.rbtn3.setDisabled(True)
        self.rbtn1.clicked.connect(self.rbtn1setLabelText)
        self.rbtn2.clicked.connect(self.rbtn1setLabelText)
        self.rbtn3.clicked.connect(self.rbtn3setLabelText)

        self.timerlbl = QLabel(self)
        self.timer1 = TimerThread()
        self.timer4 = QTimer(self)
        self.timer4.start()
        self.timer4.timeout.connect(self.Threadconnect)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.rbtn1)
        hbox.addStretch()
        hbox.addWidget(self.rbtn2)
        hbox.addStretch()
        hbox.addWidget(self.rbtn3)
        hbox.addStretch()
        hbox.addWidget(self.timerlbl)
        hbox.addStretch()
        hbox.setAlignment(Qt.AlignCenter)

        groupbox.setLayout(hbox)

        return groupbox

    def Threadconnect(self):
        sender = self.sender()
        if id(sender) == id(self.timer4):
            self.timerlbl.setText(str(self.timer1.tm))
            if self.timer1.tm == 0:
                self.timerlbl.setText('')
                self.th.start()
                self.timer1.b = 0

                self.rbtn2.setChecked(True)

    def createProgressBarGroup(self):
        groupbox = QGroupBox('운행 상황')

        self.pbar = QProgressBar(self)
        self.th = PbarThread()
        self.th.change_value.connect(self.pbar.setValue)
        self.timer2 = QTimer(self)
        self.timer2.start()
        self.timer2.timeout.connect(self.pbarAction)

        self.frm = QFrame(self)
        self.col = 'black'
        self.frm.setStyleSheet('background-color: %s' % self.col)
        self.frm.setFrameShape(QFrame.Box)
        self.frm.setFixedSize(30, 30)
        self.btn = QPushButton('해제', self)
        self.btn.clicked.connect(self.btnClick)
        self.btn.setDisabled(True)
        self.pbarAction()

        hbox = QHBoxLayout()
        hbox.addWidget(self.pbar)
        hbox.addWidget(self.frm)
        hbox.addWidget(self.btn)

        groupbox.setLayout(hbox)

        return groupbox



    def pbarAction(self):
        sender = self.sender()
        if id(sender) == id(self.timer2):
            if self.th.isRunning():
                if self.pbar.value() < 60:
                    self.col = 'green'
                    self.frm.setStyleSheet('background-color: %s' % self.col)
                elif self.pbar.value() == 60:
                    self.col = 'orange'
                    self.frm.setStyleSheet('background-color: %s' % self.col)
                elif self.pbar.value() == 70:
                    self.col = 'red'
                    self.frm.setStyleSheet('background-color: %s' % self.col)
                elif self.pbar.value() == 100:
                    self.th.a = 0
                    self.btn.setDisabled(False)

    def btnClick(self):
        self.timer1.tm = 6
        self.timer1.start()
        self.th.cnt = -1
        self.th.a = 1
        self.timer1.b = 1
        self.pbar.reset()
        self.timer4.timeout.connect(self.Threadconnect)
        self.rbtn1.setChecked(True)
        self.btn.setDisabled(True)

    def createTextLabelGroup(self):
        groupbox = QGroupBox('현재 상태')

        self.lbl1 = QLabel(self)
        self.lbl2 = QLabel('정상 운행중', self)

        self.timer3 = QTimer(self)
        self.timer3.start()
        self.timer3.timeout.connect(self.checkTime)

        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl1)
        hbox.addStretch()
        hbox.addWidget(self.lbl2)

        groupbox.setLayout(hbox)

        return groupbox

    def checkTime(self):
        sender = self.sender()
        self.CurrentDateTime = QDateTime.currentDateTime().toString("yy년 MM월 dd일 HH시 mm분 ss초")

        if id(sender) == id(self.timer3):
            self.lbl1.setText('%s' % self.CurrentDateTime)

    def rbtn1setLabelText(self):
        self.lbl2.setText('정상 운행중')

    def rbtn3setLabelText(self):
        self.lbl2.setText('운행 대기')

    def createComboBoxGroup(self):
        groupbox = QGroupBox('기능 점검')

        self.cb1 = QComboBox(self)
        self.cb1.addItem('미실행')
        self.cb1.addItem('실행')

        self.cb2 = QComboBox(self)
        self.cb2.setDisabled(True)
        self.cb2.addItem('미동작')
        self.cb2.addItem('LED 동작')
        self.cb2.addItem('차단바 동작')

        self.cb3 = QComboBox(self)
        self.cb3.setDisabled(True)
        self.cb1.activated[str].connect(self.cb2onActivated)
        self.cb2.activated[str].connect(self.cb3onActivated)

        hbox = QHBoxLayout()
        hbox.addWidget(self.cb1)
        hbox.addWidget(self.cb2)
        hbox.addWidget(self.cb3)
        groupbox.setLayout(hbox)

        return groupbox

    def cb2onActivated(self):
        if self.cb1.currentIndex() == 1:
            self.rbtn3setLabelText()
            self.cb2.setDisabled(False)
            self.rbtn3.setChecked(True)
        else:
            self.cb2.setCurrentIndex(0)
            self.cb2.setDisabled(True)
            self.rbtn1.setChecked(True)
            self.rbtn1setLabelText()

    def cb3onActivated(self):
        if self.cb2.currentIndex() != 0:
            self.cb3.setDisabled(False)
            if self.cb2.currentIndex() == 1:
                self.cb3.clear()
                self.cb3.addItem('미동작')
                self.cb3.addItem('빨간 LED')
                self.cb3.addItem('노란 LED')
                self.cb3.addItem('초록 LED')
            elif self.cb2.currentIndex() == 2:
                self.cb3.clear()
                self.cb3.addItem('차단')
                self.cb3.addItem('개방')
        else:
            self.cb3.clear()
            self.cb3.setCurrentIndex(0)
            self.cb3.setDisabled(True)

    def pbtnClicked(self):
        input_state = GPIO.input(pbtn)
        if self.rbtn1.isChecked() and input_state == False:
            self.rbtn3.setChecked(True)
            self.p.ChangeDutyCycle(2.5)
        if self.rbtn2.isChecked() and input_state == False:
            self.th.wait()
            self.rbtn3.setChecked(True)
            self.p.ChangeDutyCycle(2.5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
