import os
import Adafruit_DHT as dht
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import sys
import time
from datetime import datetime
import time
import pandas as pd

## Temperatursensor
sensor = dht.DHT22
pin = '21' # GPIO21 --> PIN40

## Feuchtesensoren
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1


run = 1

try:
    df = pd.read_csv('temp.csv')

    print('data imported')
except:
    print('no data exist, create new dataframe')
    df = pd.DataFrame(columns=['Cnt',
                               'Zeit',
                               'Temp',
                               'Humidity',
                               'Boden1',
                               'Boden2',
                               'Boden3',
                               'Boden4'])
    df.to_csv('temp.csv', index = False)
cnt = df.shape[0]
values = [0]*4

while run==1:
    cnt +=1
    humidity, temperature = dht.read_retry(sensor, pin)
    for i in range(4):
        values[i] = adc.read_adc(i, gain=GAIN)
    
    acttime = datetime.now().strftime('%H:%M:%S')
    print('Zeit: ' +time.strftime('%H:%M:%S',time.localtime()))
    print('-'*10)
    print('Temp=%2.2f °C' % temperature)
    print('Humidity= %2.2f' % humidity)
    print('-'*10)  
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    print('Counter:' + str(cnt))
    print('-'*10)
    newdata = [cnt, acttime, round(temperature, 2), round(humidity, 2), values[0],
               values[1],values[2],values[3]]
    df.loc[cnt] = newdata
    
    if cnt%60==0:
        df.to_csv('temp.csv', index = False)
        print('Speichern')
    time.sleep(1)


