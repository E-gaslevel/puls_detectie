import serial
from sys import exit
import os


try:
    ser = serial.Serial('COM6', baudrate=9600, timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8)
except Exception as e:
    print(e)
    exit("Couldn't connect!")

#Read UART
line = (ser.readline().decode('ascii').strip())
# Split received string by comma
values = line.split(',')


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
    

