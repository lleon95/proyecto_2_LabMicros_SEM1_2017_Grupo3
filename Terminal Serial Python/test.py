import serial
ser = serial.Serial('COM3',9600)
ser.write("Hola. Soy Python")
print("He enviado: Hola. Soy Python")
print("He recibido: " + ser.readline())
    
