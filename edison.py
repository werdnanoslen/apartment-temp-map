#!/usr/bin/env python

import mraa
import time
from datetime import datetime
import csv
import sys

led = mraa.Gpio(6);
button = mraa.Gpio(4);
light = mraa.Aio(0);
temp = mraa.Aio(3);

button.dir(mraa.DIR_IN)
led.dir(mraa.DIR_OUT)

rows = 0
filename = '/home/root/' + str(datetime.now()) + '.csv'
file = open(filename, 'w')
with file:
    writer = csv.writer(file)
    writer.writerow(['time', 'light', 'temp']) # header

    def blink():
        time.sleep(0.1)
        led.write(not led.read())
        time.sleep(0.1)
        led.write(not led.read())

    def record():
        date = str(datetime.now())
        lightValue = light.read()
        tempValue = temp.read()
        row = [date, lightValue, tempValue]
        writer.writerow(row)
        global rows
        rows += 1

    while True:
        for x in range(60):
            if (rows >= 1440): # after 24 hours (60*24)
                led.write(1)
                sys.exit()
            elif (x%60 == 0): # every minute
                record()
                blink()
            elif (x%5 == 0): # every 5 seconds
                blink()
            time.sleep(1)
