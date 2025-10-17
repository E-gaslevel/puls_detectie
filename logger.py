import serial
import serial.tools.list_ports

from sys import exit
import os
import string


def connect_UART():
    ports = list(serial.tools.list_ports.comports())
    try:
        for p in ports:
            if 'CP210' in p.description:
                ser = serial.Serial(p.device, 
                                    baudrate=115200, 
                                    timeout=None, 
                                    parity=serial.PARITY_NONE, 
                                    stopbits=serial.STOPBITS_ONE, 
                                    bytesize=8)
                print(f"Connected to {p.description}")
                return ser 
    except Exception as e:
        print(e)
        exit("Couldn't connect!")
        
# This function sends over UART the sample parameters, C program will read those and assign those value
# Filename is also msg to uC
def send_parameter_UART(ser, sample):
    filename = f"f{sample[0]}d{sample[1]}n{sample[2]}\n"
    print(f"File name will be {filename}")
    ser.write(filename.encode())
    return filename
    
def read_UART_and_save(ser, _filename):
    #Read UART
    line = (ser.readline().decode('ascii').strip())
    line = ''.join(ch for ch in line if ch in string.printable)
    # Split received string by comma
    values = line.split(',')

    # Check for new filename, dont overwrite old reading file, add index_number to filename
    count = 0
    filename = _filename + "_" + str(count)
    while True:
        if os.path.exists(filename):
            count += 1
            filename = filename + "_" + count
        else:
            file_to_save = os.path.join("readings", f"{filename}.txt")
            break
        

    # Write to .txt
    with open(file_to_save, "w") as file:
        file.write('\n'.join(values))
    
if __name__ == "__main__":
    ser = connect_UART()
    
    # Voer hier sample parameters, every list is a new measurement 
    parameters = [[50000, 100, 2], [20000, 50, 1]]
    for p in parameters:
        filename = send_parameter_UART(ser, p)
        read_UART_and_save(ser, filename)