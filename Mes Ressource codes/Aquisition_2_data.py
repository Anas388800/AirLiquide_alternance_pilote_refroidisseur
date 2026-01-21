# -*- coding: utf-8 -*-
"""
The purpose of this program is to recover the samples of the
arduino due and to apply signal processing.The aim is to display 
the signal retrieved by the serial port and display it on the window

EDIT : At present, the program sometimes crashes at the level of data transfer, under investigation ...

"""

#!/usr/bin/python
import serial
import matplotlib.pyplot as plt
from drawnow import *
import numpy as np
from scipy.fft import fft, fftfreq
import math
import time
# ----------------------------------------------------------------
def goertzel(samples, t, freqs):
    total_point= len(samples)
    t = np.linspace(0, total_point/Fech, total_point)
    results = []
    w_real, w_imag = [] ,[]

    for f in freqs:
        '''  Cosine and sin computation  '''
        w_real = np.cos(2.0 * math.pi * f* t)
        w_imag = np.sin(2.0 * math.pi * f *t )
        
        '''  Computation  '''
        x  = np.multiply(samples , w_real)
        y  = np.multiply(samples , w_imag)
        
        '''  Average computaion  '''  
        xavr = np.average( x)     
        yavr = np.average( y)     

        '''  Module computaion  '''          
        module = round(2 * np.sqrt(xavr**2 + yavr**2),2)
        results.append(module)   
    return results

# ----------------------------------------------------------------

ser = serial.Serial('COM4',57600) # Windows
ser.close()
ser.open() # this will also reboot the arduino

plt.ion() # initial an interractive figure

pico_data = []
dac_output = []
data_array = []

Sample = 512
Fech = 12000 #kHz
Tech = 1/Fech
"""
   not found a way to get a timestamp ... right now !, 
   so we create a time vector assuming the jitter is 3us
"""
elapsed_time = Sample * 1/Fech
t = np.arange(0, elapsed_time, 1/Fech)


"""
caractéristiques du signal
"""   
TAB_FREQ = []
f_wanted=300
freqs = TAB_FREQ

c=0

for i in range(1, 8):
    TAB_FREQ.append(i*f_wanted)

def makeFig():
  
    # Ploting slave and master signal
  
    plt.subplot(3,1,1)
    plt.plot(pico_data, 'r-', label='Sample [V]')
    # plt.title("Data acquisition with Arduino")
    # plt.ylabel("Voltage [V]")
    # plt.xlabel("Frequency [Hz]")
    # plt.grid(which='minor',color='lightblue',linestyle='--')
    # plt.grid(which='major',color='black')
    # plt.minorticks_on()
    
     
    plt.subplot(3,1,3)
    plt.plot(dac_output,'r-', label='Sample [V]')
    plt.title("power in spectral domain")
    plt.grid(which='minor',color='lightblue',linestyle='--')
    plt.minorticks_on()
    
    plt.pause(0.2)
    """ 
    plt.subplot(3,1,2)  
    plt.xlim(0,1000)
    plt.plot(xf, 2.0/Sample * np.abs(yf[0:Sample//2])) 
    plt.title("Spectral Domain FFT")
    plt.ylabel("Magnitude")
    plt.xlabel("Frequency [Hz]")
    plt.grid(which='minor',color='lightblue',linestyle='--')
    plt.grid(which='major',color='black')
    plt.minorticks_on()
    """ 
try:
    while True:
        

        data = ser.readline().decode().replace('\r','').replace('\n','')
        data_array = data.split(',')
        osci = float(data_array[0])
        dac = float(data_array[1])
        pico_data.append(osci)
        dac_output.append(dac)
        
        if (len(dac_output) == Sample):
            drawnow(makeFig)
            pico_data.clear()   
            dac_output.clear() 
            plt.clf()
        #print(data)

        """
            if ValueError:
                pass # do nothing
            """        
except KeyboardInterrupt:
    ser.close()
    print("serial connection closed")
    
"""except ValueError:
    ser.close()
    print("serial connection closed")"""
    
