
# -*- coding: utf-8 -*-
"""
"""

#!/usr/bin/python
import serial
import matplotlib.pyplot as plt
from drawnow import *
plt.ion() # ???? initial a figure
i=0
cnt=0
ser = serial.Serial('COM3',115200) # Windows
#ser = serial.Serial('/dev/ttyAMA0',9600) # Raspi

ser.close()
ser.open() # this will also reboot the arduino
data = float(ser.readline()
             .decode()
             .replace('\r', '')
             .replace('\n', '')) # first data will not be plotted

data = 0

def makeFig():
    plt.plot(i,data, 'to-')
    
try:
    while True:
        data =  float(ser.readline().decode().replace('\r','').replace('\n',''))

        plt.title('serial reader: ' + str(data), loc='left')
        plt.plot(data,'ro-') # pyplot will add this data
        plt.draw() # update plot

    
       # plt.grid(which='minor',color='lightblue',linestyle='--')
       # plt.minorticks_on()


        plt.pause(0.0001) # pause
        cnt = cnt+1
        if(cnt>50):
            data.pop(0)#keep the plot fresh by deleting the data at position 0
except KeyboardInterrupt:
    ser.close()
    print("serial connection closed")
    #plt.close()
    
"""   
    ################################################################################
# showdata.py
#
# Display analog data from Arduino using Python (matplotlib)
# 
# electronut.in
#
################################################################################

import time
import matplotlib.pyplot as plt
from drawnow import *
import serial
val = [ ]
cnt = 0
#create the serial port object
port = serial.Serial('COM3', 115200, timeout=0.5)
plt.ion()

#create the figure function
def makeFig():
    plt.ylim(0,700)
    plt.title('Osciloscope')
    plt.grid(True)
    plt.ylabel('data')
    plt.plot(val, 'ro-', label='Channel 0')
    plt.legend(loc='lower right')

while (True):
    port.write(b's') #handshake with Arduino
    if (port.inWaiting()):# if the arduino replies
        value = float(port.readline())# read the reply
#        print(value)#print so we can monitor it
#        number = int(value) #convert received data to integer 
#        print('Channel 0: {0}'.format(number))
        # Sleep for half a second.
#        time.sleep(0.01)
#        val.append(int(number))
        val.append(value)
        drawnow(makeFig)#update plot to reflect new data input
        plt.pause(.0001)
        cnt = cnt+1
    if(cnt>50):
        val.pop(0)#keep the plot fresh by deleting the data at position 0
        """