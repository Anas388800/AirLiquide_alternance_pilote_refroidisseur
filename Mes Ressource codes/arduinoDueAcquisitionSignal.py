
import serial
import numpy
import time
import threading
            
class Arduino:
    def __init__(self,port):
        self.ser = serial.Serial('COM3',19200)
        time.sleep(2)
        self.ACQUISITION = 104
        self.STOP_ACQUISITION = 105
        self.clockFreq = 42.0e6 # frequence d'horloge
        self.TAILLE_BLOC = 256
        self.TAILLE_BLOC_INT8 = self.TAILLE_BLOC*2
        
    def close(self):
        self.ser.close()
             
    def write_int8(self,v):
        self.ser.write((v&0xFF).to_bytes(1,byteorder='big'))

    def write_int16(self,v):
        v = numpy.int16(v)
        char1 = int((v & 0xFF00) >> 8)
        char2 = int((v & 0x00FF))
        self.ser.write((char1).to_bytes(1,byteorder='big'))
        self.ser.write((char2).to_bytes(1,byteorder='big'))
        
    def write_int32(self,v):
        v = numpy.int32(v)
        char1 = int((v & 0xFF000000) >> 24)
        char2 = int((v & 0x00FF0000) >> 16)
        char3 = int((v & 0x0000FF00) >> 8)
        char4 = int((v & 0x000000FF))
        self.ser.write((char1).to_bytes(1,byteorder='big'))
        self.ser.write((char2).to_bytes(1,byteorder='big'))
        self.ser.write((char3).to_bytes(1,byteorder='big'))
        self.ser.write((char4).to_bytes(1,byteorder='big'))       
              
    def lancer_acquisition(self,voies,gains,offsets,fechant,nb):
        ticks = int(self.clockFreq/fechant)
        self.write_int8(self.ACQUISITION)
        self.nvoies = nv = len(voies)
        self.write_int8(nv)
        for k in range(nv):
            self.write_int8(voies[k])
        for k in range(nv):
            self.write_int8(gains[k])
        for k in range(nv):
            self.write_int8(offsets[k])
        self.write_int32(ticks)
        self.write_int32(nb)
              
    def stopper_acquisition(self):
        self.write_int8(self.STOP_ACQUISITION)
              
    def lecture(self):
        buf = self.ser.read(self.TAILLE_BLOC_INT8)
        data = numpy.zeros(self.TAILLE_BLOC,dtype=numpy.float32)
        j = 0
        for i in range(self.TAILLE_BLOC):
        	data[i] = buf[j]+0x100*buf[j+1]
        	j += 2
        return data
              
class AcquisitionThread(threading.Thread): 
    def __init__(self,arduino,voies,gains,offsets,fechant,nblocs,npaquets):
        threading.Thread.__init__(self)
        self.arduino = arduino
        self.nvoies = len(voies)
        self.voies = voies
        self.gains = gains
        self.offsets = offsets
        self.fechant = fechant
        self.running = False
        self.nblocs = nblocs # nombre de blocs dans un paquet
        self.npaquets = npaquets
        self.taille_bloc = arduino.TAILLE_BLOC
        self.taille_paquet = self.taille_bloc * self.nblocs
        self.data = numpy.zeros((self.nvoies,self.nblocs*arduino.TAILLE_BLOC*self.npaquets))
        self.compteur_paquets = 0
        self.compteur_paquets_lus = 0
        self.nechant = 0
              
    def run(self):
        self.arduino.lancer_acquisition(self.voies,self.gains,self.offsets,self.fechant,0) # acquisition sans fin
        self.running = True
        indice_bloc = 0
        while self.running:
            i = self.compteur_paquets*self.taille_paquet +indice_bloc*self.taille_bloc
            j = i+self.taille_bloc
            for v in range(self.nvoies):
                self.data[v,i:j] = self.arduino.lecture()
            self.nechant = j
            indice_bloc += 1
            if indice_bloc==self.nblocs:
                indice_bloc = 0
                self.compteur_paquets += 1
                if self.compteur_paquets==self.npaquets:
                    self.stop()
               
    def stop(self):
        self.running = False
        time.sleep(1)
        #self.join()
        self.arduino.stopper_acquisition()
               
    def paquet(self): # obtention du dernier paquet
        if self.compteur_paquets==self.compteur_paquets_lus:
            return -1
        i = self.compteur_paquets_lus*self.taille_paquet
        j = i+self.taille_paquet                    
        self.compteur_paquets_lus += 1
        return self.data[:,i:j]
               
    def echantillons(self,nombre):
        j = self.nechant
        i = j-nombre
        if i<0: i=0
        if j-i<=0: return (-1,-1,-1)
        temps = numpy.arange(j-i)/self.fechant
        tmax = nombre/self.fechant
        return (temps,self.data[:,i:j],tmax)
                