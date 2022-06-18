from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QSize, Qt

import os
import sys

import Adafruit_DHT as dht
import RPi.GPIO as GPIO
import sys
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt


sensor = dht.DHT22
pin = '21'
GPIO.setmode(GPIO.BCM)
pin_relais_1 = 20
GPIO.setup(pin_relais_1, GPIO.OUT)

class main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        QMainWindow.__init__(self)
        self.setFixedWidth(500)
        self.setWindowTitle('Garten App')
        main_layout = QHBoxLayout()
        button_layout = QVBoxLayout()
        info_layout = QVBoxLayout()
        
        main_layout.addLayout(button_layout)
        main_layout.addLayout(info_layout)
        
        #self.button = QPushButton('Push')
        #self.button.clicked.connect(self.changeRelais)
        #self.setMinimumSize(QSize(800, 400))
        #button_layout.addWidget(self.button)
        
        #self.send_sms = QPushButton('SMS')
        #self.send_sms.clicked.connect(self.SendSms)
        #self.setFixedSize(QSize(400, 200))
        #button_layout.addWidget(self.send_sms)
        
        #self.Anzahl = QLabel(' ')
        #self.setFixedSize(QSize(200, 200))
        #button_layout.addWidget(self.Anzahl)
        
        #self.Temp = QPushButton('Meas')
        #self.setFixedSize(QSize(200, 200))
        #self.Temp.clicked.connect(self.temp)
        #button_layout.addWidget(self.Temp)
        
        #self.Hum = QLabel('')
        #self.setFixedSize(QSize(200, 200))
        #button_layout.addWidget(self.Hum)
        
        #self.active = QLabel('')
        #self.setFixedSize(QSize(200, 200))
        #button_layout.addWidget(self.active)
        
        #widget = QWidget()
        #widget.setLayout(pagelayout)
        #self.setCentralWidget(widget)
        
        self.cnt = 0
        self.meas = 0
        
    def changeRelais(self):
        
        self.cnt += 1
        if self.cnt %2:
            GPIO.output(pin_relais_1, GPIO.LOW)
            self.active.setStyleSheet('background-color: green')
            self.button.setStyleSheet('background-color: green')
            
        else:
            GPIO.output(pin_relais_1, GPIO.HIGH)
            self.active.setStyleSheet('background-color: red')
            self.button.setStyleSheet('background-color: red')
            
        self.Anzahl.setText(str(self.cnt))
        
        
    
    def SendSms(self):
        pass
    
    def temp(self):
        for i in range(1, 20):
            print(i)
            humidity, temperature = dht.read_retry(sensor, pin)
            print('Humidity= %2.2f' % humidity)
            print('Temp=%2.2f °C' % temperature)
            self.Temp.setText('Temp=%2.2f °C' % temperature)
            self.Hum.setText('Humidity= %2.2f' % humidity)
            #self.Anzahl.setText(str(i))
            time.sleep(2.0)
            
app = QApplication(sys.argv)
window = main()
window.show()

app.exec_()

            