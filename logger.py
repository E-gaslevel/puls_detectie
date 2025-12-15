import serial
from serial import Serial
import serial.tools.list_ports

from sys import exit
from time import sleep
import os

def connect_UART():
    # Connects to uC using pySerial, finds automatically the right device
    ports = list(serial.tools.list_ports.comports())
    try:
        for p in ports:
            if 'CP210' in p.description:
                ser = serial.Serial(p.device, 
                                    baudrate=921600, 
                                    timeout=1, 
                                    parity=serial.PARITY_NONE, 
                                    stopbits=serial.STOPBITS_ONE, 
                                    bytesize=8)
                print(f"Connected to {p.description}")
                return ser 
    except Exception as e:
        print(e)
        exit("Couldn't connect!")
        
def send_parameter_UART(ser, sample):
    # This function sends over UART the sample parameters, C program will read those and assign those values to the measurement
    filename_wo_index = f"f{sample[0]}d{sample[1]}n{sample[2]}"
    print(f"Sending parameters: frequency: {sample[0]}, duty cycle: {sample[1]}, number of pulses: {sample[2]}")
    ser.write(f"{filename_wo_index}\n".encode())
    return filename_wo_index
    
def read_UART_and_save(ser, filename_wo_index):
    print("start read line")
    assert isinstance(ser, Serial)

    values = []
    temp = ""

    while len(values) < 4000:
        n = ser.in_waiting
        if not n:
            continue

        chunk = ser.read(n).decode("ascii")
        temp += chunk

        # split complete lines
        lines = temp.split('\n')
        for line in lines[:-1]:
            values.append(line + '\n')
            if len(values) >= 4000:
                break

        # keep unfinished line
        temp = lines[-1]

    # while (len(values) < 4000) and (value := ser.readline()):
    #     values.append(value.decode("ascii"))
    sleep(0.5)
    count = 0
    while True:
        file_to_save = os.path.join("readings1", f"test_{filename_wo_index}_{count}.txt")
        if os.path.exists(file_to_save):
            count += 1
        else:
            break
    print("file made")

    with open(file_to_save, "w") as file:
        file.write(''.join(values))
        print(f"Data saved to {file_to_save}")
    print("print write")
    
if __name__ == "__main__":
    ser = connect_UART()
    
    # Fill parameters in, every inner list is a new measurement, C program will wait for those and run forever
    parameters = [
        [10000, 25, 1], [10000, 25, 3], [10000, 25, 8],
        [10000, 50, 1], [10000, 50, 3], [10000, 50, 8],
        [10000, 75, 1], [10000, 75, 3], [10000, 75, 8],
        [110000, 25, 1], [110000, 25, 3], [110000, 25, 8],
        [110000, 50, 1], [110000, 50, 3], [110000, 50, 8],
        [110000, 75, 1], [110000, 75, 3], [110000, 75, 8],
        [210000, 25, 1], [210000, 25, 3], [210000, 25, 8],
        [210000, 50, 1], [210000, 50, 3], [210000, 50, 8],
        [210000, 75, 1], [210000, 75, 3], [210000, 75, 8],
        [310000, 25, 1], [310000, 25, 3], [310000, 25, 8],
        [310000, 50, 1], [310000, 50, 3], [310000, 50, 8],
        [310000, 75, 1], [310000, 75, 3], [310000, 75, 8],
        [410000, 25, 1], [410000, 25, 3], [410000, 25, 8],
        [410000, 50, 1], [410000, 50, 3], [410000, 50, 8],
        [410000, 75, 1], [410000, 75, 3], [410000, 75, 8],
        [510000, 25, 1], [510000, 25, 3], [510000, 25, 8],
        [510000, 50, 1], [510000, 50, 3], [510000, 50, 8],
        [510000, 75, 1], [510000, 75, 3], [510000, 75, 8],
        [610000, 25, 1], [610000, 25, 3], [610000, 25, 8],
        [610000, 50, 1], [610000, 50, 3], [610000, 50, 8],
        [610000, 75, 1], [610000, 75, 3], [610000, 75, 8],
        [710000, 25, 1], [710000, 25, 3], [710000, 25, 8],
        [710000, 50, 1], [710000, 50, 3], [710000, 50, 8],
        [710000, 75, 1], [710000, 75, 3], [710000, 75, 8],
        [810000, 25, 1], [810000, 25, 3], [810000, 25, 8],
        [810000, 50, 1], [810000, 50, 3], [810000, 50, 8],
        [810000, 75, 1], [810000, 75, 3], [810000, 75, 8],
        [910000, 25, 1], [910000, 25, 3], [910000, 25, 8],
        [910000, 50, 1], [910000, 50, 3], [910000, 50, 8],
        [910000, 75, 1], [910000, 75, 3], [910000, 75, 8],
        [1000000, 25, 1], [1000000, 25, 3], [1000000, 25, 8],
        [1000000, 50, 1], [1000000, 50, 3], [1000000, 50, 8],
        [1000000, 75, 1], [1000000, 75, 3], [1000000, 75, 8]
    ]
    for p in parameters:
        filename = send_parameter_UART(ser, p)
        read_UART_and_save(ser, filename)