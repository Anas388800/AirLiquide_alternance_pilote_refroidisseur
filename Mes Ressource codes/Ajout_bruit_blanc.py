from __future__ import division
from scipy.fft import fft
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
import random



# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
plt.close('all');

#Ouverture du fichier des capteur de vibration :
data = pd.read_excel(r'R:\Also\1000763-A0500-STANDARDISATION PULSE TUBE\Working Dir\Anas\Mes Algorithmes\Bruit_blanc.xlsx');

bruit=pd.DataFrame(data, columns=['bruit']);
T=pd.DataFrame(data, columns=['temps']);



#Afichage des Vibrations
plt.figure(1);
plt.grid();
plt.title('Force : Somme Fy des 4lw cisaillement (Kevin)')
plt.ylabel('Amplitude Force [N]');
plt.plot(T,bruit);
plt.show();

t=np.linspace(0,2,5000);
bruit1=np.linspace(data['bruit'][0],data['bruit'][len(data)-1],5000)

plt.figure(2);
plt.plot(t,bruit1);
