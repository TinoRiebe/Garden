from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QSize, Qt

import os
import sys

import Adafruit_DHT as dht
import RPi.GPIO as GPIO
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt
import Adafruit_ADS1x15
import time


## Feuchtesensoren
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

## Temperatursensor
sensor = dht.DHT22
pin = '21' # GPIO21 --> PIN40


## Relais
GPIO.setmode(GPIO.BCM)
pin_relais_1 = 20
GPIO.setup(pin_relais_1, GPIO.OUT)


class main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        QMainWindow.__init__(self)
        
        self.main_size=[300, 200]
        self.cnt_bt = 2*3
        
        self.setFixedWidth(self.main_size[0])
        self.setFixedHeight(self.main_size[1])
        self.setWindowTitle('Garten App')
        main_layout = QHBoxLayout()
        button_layout = QVBoxLayout()
        info_layout = QVBoxLayout()
        self.bt_exit = QPushButton('Exit')
        self.bt_exit.clicked.connect(self.close)
        self.bt_exit.setFixedHeight(self.main_size[0]/self.cnt_bt)
        self.bt_meas_temp = QPushButton('Temp')
        self.bt_meas_temp.setFixedHeight(self.main_size[0]/self.cnt_bt)
        self.bt_meas_temp.clicked.connect(self.meas_temp)
        button_layout.addWidget(self.bt_meas_temp)
        button_layout.addWidget(self.bt_exit)
        self.bt_send_sms = QPushButton('SMS')
        self.bt_send_sms.setFixedHeight(self.main_size[0]/self.cnt_bt)
        self.bt_send_sms.clicked.connect(self.SendSms)
        button_layout.addWidget(self.bt_send_sms)
        
        self.bt_change_relais = QPushButton('Relais')
        self.bt_change_relais.setFixedHeight(self.main_size[0]/self.cnt_bt)
        self.bt_change_relais.setStyleSheet('background-color: red')
        self.bt_change_relais.clicked.connect(self.changeRelais)
        button_layout.addWidget(self.bt_change_relais)
        
                                
        self.temp = QLabel('Temperature')
        info_layout.addWidget(self.temp)
        
        self.humi = QLabel('Humidity')
        info_layout.addWidget(self.humi)
        
        self.time = QLabel('Time')
        info_layout.addWidget(self.time)
        
        main_layout.addLayout(button_layout)
        main_layout.addLayout(info_layout)
        
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        
        self.cnt = 0
        self.meas = 0
        self.run = 1
        
    def act_time(self):
        while self.run ==1:
            self.time.setText(time.strftime('%d-%m %H:%M:%S',time.localtime()))
            time.sleep(1)
        
        
    def changeRelais(self):
        
        self.cnt += 1
        if self.cnt %2:
            GPIO.output(pin_relais_1, GPIO.LOW)
            self.bt_change_relais.setStyleSheet('QPushButton {background-color: green;}')
            self.time.setStyleSheet('background-color: green')
        else:
            GPIO.output(pin_relais_1, GPIO.HIGH)
            self.bt_change_relais.setStyleSheet('background-color: red')
            self.time.setStyleSheet('background-color: red')
        self.time.setText(str(self.cnt))
        
        
    
    def SendSms(self):
        cnt = 0
        
        for k in range(0, 11):
            self.time.setText(time.strftime('%d-%m %H:%M:%S',time.localtime()))
            #acttime1 = time.localtime()
            acttime = datetime.now().strftime('%H:%M:%S') # %d-%m-%Y')
            humidity, temperature = dht.read_retry(sensor, pin)
            if k %2:
                GPIO.output(pin_relais_1, GPIO.LOW)
                self.bt_change_relais.setStyleSheet('QPushButton {background-color: green;}')
                self.time.setStyleSheet('background-color: green')
                text = 'Relais ON'
            else:
                GPIO.output(pin_relais_1, GPIO.HIGH)
                self.bt_change_relais.setStyleSheet('background-color: red')
                self.time.setStyleSheet('background-color: red')
                text = 'Relais OFF'
                
            print('Zeit: ', acttime)
            values = [0]*4
            for i in range(4):
                values[i] = adc.read_adc(i, gain=GAIN)
            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
            print('Humidity= %2.2f' % humidity)
            print('Temp=%2.2f °C' % temperature)
            print(text)
            self.temp.setText('Temp=%2.2f °C' % temperature)
            time.sleep(2)
        
       # for i in range(0, 100):
        #    acttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       #     humidity, temperature = dht.read_retry(sensor, pin)
       #     if temperature > 24:
       #         GPIO.output(pin_relais_1, GPIO.HIGH)
       #     else:
       #         GPIO.output(pin_relais_1, GPIO.LOW)
       # 
       #     cnt += 1
       #     print('Messung ', str(cnt))
       #     print('Zeit: ', acttime)
       #     print('Humidity= %2.2f' % humidity)
       #     print('Temp=%2.2f °C' % temperature)
       #     time.sleep(1.0)
   
    def meas_temp(self):
        humidity, temperature = dht.read_retry(sensor, pin)
        #newdata = [round(temperature, 2), round(humidity, 2)]
        self.temp.setText('Temp=%2.2f °C' % temperature)
        self.humi.setText('Humidity= %2.2f' % humidity)
        self.time.setText(time.strftime('%d-%m %H:%M:%S',time.localtime()))
        #plt.plot(newdata[0].tolist(),'--b',label='Temp')
        #plt.plot(newdata[1].tolist(),'--r', label='Humidiy')
        #plt.ylim(0, 100)
        #plt.legend()
        #plt.pause(0.05)

        time.sleep(1.0)
            
app = QApplication(sys.argv)
window = main()
window.show()

app.exec_()

            
