import serial
from tkinter import *
# import sys
import numpy as np
import re

# import string

premierMarqu = False
m = np.zeros(50, float)
marqueur = "ANG"
marqueurs = [["DCM", "ANG", "AN", "THI"], ['X', 'Y', 'Z', "MX", "MY", "MZ", "?X", "?Y", "?Z"],
             ["Roll:Roulis", "Pitch:Elevation", "Yaw:Lacet"],
             ["Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z", "Magnetom X", "Magnetom Y"
                 , "Magnetom Z"],
             ["Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z", "Magnetom X", "Magnetom Y", "Magnetom Z",
              "TEMP:"]]
elementsaFiltrer = ["n", 'r', 'b', "\\", "'", ",DCM:", ",THI:", "TMP:,", ",AN", "C", "M", ":"]
entete = []

RawData = ""  # variable contenant la ligne envoyé par le port serie
curs = 0  # curseur qui pointe les données entre les marqueurs


# lit les données
def tempo():
    global RawData
    global premierMarqu
    global marqueur

    if premierMarqu:
        decodeserial()
    else:
        while marqueur not in str(RawData):
            RawData = ser.readline()
            # #print("not flushed")
        premierMarqu = True  # premiers élements parasites filtrés

    RawData = ser.readline()
    print("Donnees :", RawData)  # ##print a string
    placevaleurs()
    root.after(1, tempo)


def decodeserial():
    global curs
    global RawData
    global m
    # lstDat = str(RawData).split(',')
    floatArray = []
    # epurSplit = "0"
    # sommeFloat = 0

    # #print (lstDat)
    print("chaine épurée", epurchaine2())
    epurSplit = epurchaine2().split(',')

    for n in range(len(np.asarray(epurSplit))):
        n = n
        # #print("chaine splitéé",np.asarray(epurSplit)[n])

    if np.asarray(epurSplit)[0] != '':
        try:

            floatArray = np.asarray(epurSplit).astype(float)
            # #print("len",len(floatArray))
        except:
            print("erreur")

    else:
        return
    # #print("len",len(floatArray))

    for z in range((len(floatArray))):
        m[z] = floatArray[z]
        # #print("index",z,"curs",curs,"m ",m)
    # #print(len(floatArray))
    curs += 1


def epurchaine2():
    global elementsaFiltrer
    global RawData
    chepur = str(RawData)

    chepur = re.sub('[^0-9,.-]', '', chepur)
    chepur = re.sub('^[,]', '', chepur)
    chepur = re.sub('[,]$', '', chepur)
    chepur = re.sub("[,]{2}", ',', chepur)
    # for d in elementsaFiltrer:
    #    chepur = chepur.replace(d, "")
    print("chepur2", chepur)
    # chepur = chepur.replace(" ",",")#mets une virgule entre les chaines

    return chepur


def placevaleurs():
    global m
    global vars
    for f in range(len(m)):
        vars[f % 9].set(m[f % 9])


def on_closing():
    ser.close()  # close port
    root.destroy()


# Les Initialisations
# Port serie
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
ser.baudrate = 115200
# #print(ser.name)         # check which port was really used


# premiere lecture du port serie pour dimensionner la fenetre.
# noinspection SyntaxErrro
if not premierMarqu:
    while marqueur not in str(RawData):# a MODIFIER
        RawData = ser.readline()
        # #print("not flushed")
    premierMarqu = True  # premiers élements parasites filtrés
    print(str(RawData))
for t in range(4):

    for i, y in enumerate(marqueurs[0]):
        print("cherche", y, i)
        if (y in str(RawData)) and y != "":
            print("trouvé", str(RawData).find(y))
            for t in marqueurs[i + 1]:
                entete.append(t)
                marqueurs[0][i] = ""
RawData = ser.readline()
print(entete, marqueurs[0])
# Fenetre d'affichage
root = Tk()
root.title("Matrice DCM")
r = 0
vars = []
text = StringVar()
for col, item in enumerate(['X', 'Y', 'Z', "MX", "MY", "MZ", "?X", "?Y", "?Z"]):
    vars.append(StringVar())
    l = Label(root, text=item, width=10)
    e = Label(root, textvariable=vars[-1], width=10)
    l.grid(row=(col % 3), column=(col // 3) * 2)
    e.grid(row=(col % 3), column=((col // 3) * 2) + 1)

# boucle d'événement sur tempo
root.after(30, tempo)

root.protocol("WM_DELETE_WINDOW", on_closing)

# boucle principale
root.mainloop()

ser.close()  # close port
for i, j in enumerate(marqueur):
    print(j)
