import serial
import serial.tools.list_ports

import numpy as np
import matplotlib.pyplot as plt

from sys import exit
import os

data_number = []

ports = list(serial.tools.list_ports.comports())
try:
    for p in ports:
        if 'CP210' in p.description:
            ser = serial.Serial(p.device, 
                                baudrate=9600, 
                                timeout=None, 
                                parity=serial.PARITY_NONE, 
                                stopbits=serial.STOPBITS_ONE, 
                                bytesize=8)
            print(f"Connected to {p.description}")
except Exception as e:
    print(e)
    exit("Couldn't connect!")

#Read UART
line = (ser.readline().decode('ascii').strip())
# Split received string by comma
values = line.split(',')
for v in values:
    try:
        data_number.append((int(v)/4095)*1.25)
    except ValueError:
        pass

# Check for new filename, dont overwrite old reading file
count = 0
while True:
    filename = os.path.join("readings", f"reading{count}.txt")
    if not os.path.exists(filename):
        break
    count += 1

# Write to .txt
with open(filename, "w") as file:
    file.write('\n'.join(values))
    
x = np.arange(0., 5000., 1)

plt.axis([0, 5000, -0.1, 1.3])
plt.plot(x, data_number)
plt.show()
    

