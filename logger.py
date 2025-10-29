import serial
import serial.tools.list_ports

from sys import exit
import os

def connect_UART():
    # Connects to uC using pySerial, finds automatically the right device
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
        
def send_parameter_UART(ser, sample):
    # This function sends over UART the sample parameters, C program will read those and assign those values to the measurement
    filename_wo_index = f"f{sample[0]}d{sample[1]}n{sample[2]}"
    print(f"Sending parameters: frequency: {sample[0]}, duty cycle: {sample[1]}, number of pulses: {sample[2]}")
    ser.write(f"{filename_wo_index}\n".encode())
    return filename_wo_index
    
def read_UART_and_save(ser, filename_wo_index):
    # The program receives all data from a measurement in one line, it will read that and split all values by commas
    # After that there will be a check if a .txt file exists, if so count+1(this way, no data is lost)
    # At last save to the given filename
    line = (ser.readline().decode('ascii').strip())
    values = line.split(',')

    count = 0
    while True:
        file_to_save = os.path.join("readings", f"50_{filename_wo_index}_{count}.txt")
        if os.path.exists(file_to_save):
            count += 1
        else:
            break

    with open(file_to_save, "w") as file:
        file.write('\n'.join(values))
        print(f"Data saved to {file_to_save}")
    
if __name__ == "__main__":
    ser = connect_UART()
    
    # Fill parameters in, every inner list is a new measurement, C program will wait for those and run forever
    parameters = [[50000, 100, 2], [20000, 50, 1], [1000, 75, 3]]
    for p in parameters:
        filename = send_parameter_UART(ser, p)
        read_UART_and_save(ser, filename)