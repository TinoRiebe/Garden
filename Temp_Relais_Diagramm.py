import Adafruit_DHT as dht
import RPi.GPIO as GPIO
import sys
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from datetime import datetime

sensor = dht.DHT22
pin = '21'

GPIO.setmode(GPIO.BCM)
pin_relais_1 = 20
GPIO.setup(pin_relais_1, GPIO.OUT)




try:
    df = pd.read_csv('temp.csv')

    print('data imported')
except:
    print('no data exist, create new dataframe')
    df = pd.DataFrame(columns=['Cnt',
                               'Datum',
                               'Temp',
                               'Humidity'])
    df.to_csv('liste.csv', index = False)
    


cnt = df.shape[0]
    
for i in range(0, 100):
    acttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    humidity, temperature = dht.read_retry(sensor, pin)
    if temperature > 24:
        GPIO.output(pin_relais_1, GPIO.HIGH)
    else:
        GPIO.output(pin_relais_1, GPIO.LOW)
        
    cnt += 1
    print('Messung ', str(cnt))
    print('Zeit: ', acttime)
    print('Humidity= %2.2f' % humidity)
    print('Temp=%2.2f °C' % temperature)
    newdata = [cnt, acttime, round(temperature, 2), round(humidity, 2)]
    df.loc[cnt] = newdata
    plt.plot(df['Temp'].tolist(),'--b',label='Temp')
    plt.plot(df['Humidity'].tolist(),'--r', label='Humidiy')
    plt.ylim(0, 100)
    #plt.legend()
    plt.pause(0.05)
    
    time.sleep(2.0)
    
plt.show()
df.to_csv('liste.csv', index = False)


