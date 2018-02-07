import sys
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
import csv
import time
import os.path

if os.path.isfile('log.csv')==False:
    open('log.csv', 'w')

# Gathering all is breaking Windows computer
timeList = []
with open('log.csv') as log:
    readCSV = csv.reader(log, delimiter=',')
    for row in readCSV:
        timeList.append(row[1])
sum = datetime.timedelta()
for i in timeList:
    (h, m, s) = i.split(':')
    d = datetime.timedelta(hours=float(h), minutes=float(m), seconds=float(s))
    sum += d
# Everything else works fine.

# LAST 7 DAYS COUNTER
date_list = []
today = datetime.date.today()
date_list.append(str(today))
counter = 0
while counter < 6:
    counter+=1
    daycounter = today - datetime.timedelta(days=counter)
    date_list.append(str(daycounter))
# SEARCH CSV FILE FOR ALL DAYS AND APPEND THE HOURS TO A LIST
weekHours = []
with open('log.csv', 'r') as lastweek:
    readCSV = csv.reader(lastweek, delimiter=',')
    for row in readCSV:
        for date in date_list:
            if date in row:
                weekHours.append(row[1])
#ADD WEEK HOURS UP
week_sum = datetime.timedelta()
for i in weekHours:
    (h, m, s) = i.split(':')
    d = datetime.timedelta(hours=float(h), minutes=float(m), seconds=float(s))
    week_sum += d

# TODAY'S HOURS
dailyHours = []
date_list = []
today = datetime.date.today()
date_list.append(str(today))
with open('log.csv', 'r') as today:
    readCSV = csv.reader(today, delimiter=',')
    for row in readCSV:
        for date in date_list:
            if date in row:
                dailyHours.append(row[1])

daily_sum = datetime.timedelta()
for i in dailyHours:
    (h, m, s) = i.split(':')
    d = datetime.timedelta(hours=float(h), minutes=float(m), seconds=float(s))
    daily_sum += d


# GUI
class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.total = QLabel('Total Hours:  '+str(sum))
        self.total.setAlignment(Qt.AlignCenter)
        self.weekly = QLabel('Weekly Hours:  '+str(week_sum))
        self.weekly.setAlignment(Qt.AlignCenter)
        self.daily = QLabel('Today\'s Hours:  '+str(daily_sum))
        self.daily.setAlignment(Qt.AlignCenter)
        self.timer = QLabel('Idle')
        self.timer.setAlignment(Qt.AlignCenter)
        self.filename = QLineEdit("File Name Here")
        self.language = QComboBox()
        self.language.addItem("Python")
        self.language.addItem("Django")
        self.language.addItem("Javascript")
        self.language.addItem("HTML")
        self.language.addItem("Unity")
        self.b1 = QPushButton('Start')
        self.b2 = QPushButton('Stop')

        v_box3 = QHBoxLayout()
        v_box3.addWidget(self.filename)
        v_box3.addWidget(self.language)

        v_box2 = QVBoxLayout()
        v_box2.addStretch()
        v_box2.addWidget(self.b1)
        v_box2.addWidget(self.b2)
        v_box2.addLayout(v_box3)

        v_box1 = QVBoxLayout()
        v_box1.addWidget(self.timer)
        v_box1.addLayout(v_box2)

        h_box1 = QVBoxLayout()
        v_box2.addStretch()
        h_box1.addWidget(self.total)
        h_box1.addWidget(self.weekly)
        h_box1.addWidget(self.daily)
        h_box1.addLayout(v_box1)

        self.setLayout(h_box1)

        self.b1.clicked.connect(lambda: self.btn_clk(self.b1, 'Hello from Clear'))
        self.b2.clicked.connect(lambda: self.btn_clk(self.b2, 'Hello from Print'))

        self.setGeometry(100, 100, 350, 200)
        self.setWindowTitle('ClockHours')
        self.setStyleSheet("background-color:white;")
        self.show()

    def btn_clk(self, b, chk):
        if b.text() == 'Start':
            self.timer.setText('Clocking Hours')
            self.setStyleSheet("background-color:#00AA4F;")
            global start
            start = datetime.datetime.now()
        else:
            today = datetime.date.today()
            self.setStyleSheet("background-color:white;")
            end = datetime.datetime.now()
            eq = end - start
            self.timer.setText(str(eq))
            name = self.filename.text()
            output = str(name), str(eq), str(self.language.currentText()), str(today)
            # APPEND ROW TO CSV
            with open("log.csv", "a") as log:
                csv_app = csv.writer(log)
                csv_app.writerow(output)

app = QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
