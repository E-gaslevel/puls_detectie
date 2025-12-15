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
                n = ser.in_waiting
                if n:
                    ser.read(n)
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

    while len(values) < 4500:
        n = ser.in_waiting
        if not n:
            continue

        chunk = ser.read(n).decode("ascii")
        temp += chunk
        
        lines = temp.split('\n')
        for line in lines[:-1]:
            values.append(line + '\n')
            if len(values) >= 4500:
                break

        temp = lines[-1]

    sleep(0.5)
    n = ser.in_waiting
    if n:
        ser.read(n)
    count = 0
    while True:
        file_to_save = os.path.join("fles4\\meting1", f"18.8_{filename_wo_index}_{count}.txt")
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

    freqs = [
        20000, 27000, 37000, 50000, 67000, 90000,
        120000, 165000, 220000, 300000, 400000, 550000, 750000, 1000000
    ]

    n_values = range(1, 9)  # 1 t/m 8
    d_values = [25, 50, 75]

    for freq in freqs:
        for d in d_values:
            for n in n_values:
                p = [freq, d, n]
                filename = send_parameter_UART(ser, p)
                read_UART_and_save(ser, filename)