import serial
port = input("Escriba el nombre del puerto: ")
baudrate = input("Escriba el baudrate: ")
ser = serial.Serial(port, baudrate)
while True:
    print ser.readline(),


