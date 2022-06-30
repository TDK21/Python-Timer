# Simple Timer
# Using Qt6 for GUI
# Author TDK21

import sys
import time
from PyQt6 import QtCore, QtWidgets

total = 0

class Countdown(QtCore.QThread):
    mySig = QtCore.pyqtSignal(QtCore.QVariant)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.running = False

    def run(self):
        self.running = True
        countdown = total
        self.func = MainWindow()
        while self.running == True:
            if countdown != 0:
                countdown -= 1
            if countdown == 0:
                self.running = False
            self.mySig.emit(countdown)
            time.sleep(1)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Timer")
        self.resize(350, 100)
        self.lcd = QtWidgets.QLCDNumber()
        self.lcd.setMinimumSize(350, 100)
        self.lcd.setDigitCount(9)
        self.hourLabel = QtWidgets.QLabel("Hours")
        self.minutesLabel = QtWidgets.QLabel("Mins")
        self.secLabel = QtWidgets.QLabel("Secs")
        self.hourLabel.setMaximumSize(50, 24)
        self.minutesLabel.setMaximumSize(50, 24)
        self.secLabel.setMaximumSize(50, 24)
        self.hourText = QtWidgets.QLineEdit("0")
        self.minuteText = QtWidgets.QLineEdit("0")
        self.secText = QtWidgets.QLineEdit("0")
        self.hourText.setMaximumSize(50, 25)
        self.minuteText.setMaximumSize(50, 25)
        self.secText.setMaximumSize(50, 25)
        self.btn = QtWidgets.QPushButton("Start")
        self.btn.setMaximumSize(101, 24)
        self.textLayout = QtWidgets.QHBoxLayout()
        self.textLayout.addWidget(self.hourLabel)
        self.textLayout.addWidget(self.minutesLabel)
        self.textLayout.addWidget(self.secLabel)
        self.horLayout = QtWidgets.QHBoxLayout()
        self.horLayout.addWidget(self.hourText)
        self.horLayout.addWidget(self.minuteText)
        self.horLayout.addWidget(self.secText)
        self.verLayout = QtWidgets.QVBoxLayout()
        self.verLayout.addWidget(self.lcd)
        self.verLayout.addItem(self.textLayout)
        self.verLayout.addItem(self.horLayout)
        self.btnLayout = QtWidgets.QHBoxLayout()
        self.btnLayout.addWidget(self.btn)
        self.verLayout.addItem(self.btnLayout)
        self.setLayout(self.verLayout)
        self.btn.clicked.connect(self.on_clicked)

        self.count = Countdown()

    def removeWidgets(self):
        self.verLayout.removeItem(self.btnLayout)
        self.verLayout.removeItem(self.textLayout)
        self.verLayout.removeItem(self.horLayout)
        self.textLayout.removeWidget(self.hourText)
        self.hourText = None
        self.textLayout.removeWidget(self.minuteText)
        self.minuteText = None
        self.textLayout.removeWidget(self.secText)
        self.secText = None
        self.btnLayout.removeWidget(self.btn)
        self.btn = None
        self.horLayout.removeWidget(self.hourLabel)
        self.hourLabel = None
        self.horLayout.removeWidget(self.minutesLabel)
        self.minutesLabel = None
        self.horLayout.removeWidget(self.secLabel)
        self.secLabel = None
        self.adjustSize()

    def on_clicked(self):
        global total
        h = self.hourText.text()
        m = self.minuteText.text()
        s = self.secText.text()
        total = int(h) * 3600 + int(m) * 60 + int(s)
        self.count.mySig.connect(self.clock)
        if not self.count.isRunning():
            self.count.start()
        self.removeWidgets()

    @QtCore.pyqtSlot(QtCore.QVariant)
    def clock(self, lcdcount):
        gotHour = lcdcount // 3600
        gotMin = lcdcount // 60 - gotHour * 60
        gotSec = lcdcount - gotMin * 60 - gotHour * 3600
        if gotHour < 10:
            gotHour = "0" + str(gotHour)
        if gotMin < 10:
            gotMin = "0" + str(gotMin)
        if gotSec < 10:
            gotSec = "0" + str(gotSec)
        result = str(gotHour) + ":" + str(gotMin) + ":" + str(gotSec)
        self.lcd.display(result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
