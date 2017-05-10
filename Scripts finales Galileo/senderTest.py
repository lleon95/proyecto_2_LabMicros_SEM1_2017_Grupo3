# Importar librerias
import serial 
import time

# Vincular puerto serial
ser = serial.Serial('/dev/tnt3', 9600)

# Constante
y =[0,4,6,-4,9,-1,0,-8,3,1,-6,8,0,2,1,0,-3,10,15,9,13,16,7,9,18,6,19,23,25,12,20,15,19,25,15,34,33,20,26,19,31,33,20,26,28,30,21,14,23,19,20,18,25,8,21,19,17,9,12,-7,7,-8,3,5,5,-10,1,2,10,9,-7,-5,-8,-10,-1,8,-9,1,-5,1,0,-8,10,10,5,-3,6,7,-4,-4,2,-1,-9,-3,4,-6,1,2,5,0]


# Para enviar el mismo paquete, 4 veces
for j in range(0,3):
  # Indicar el paquete enviado
  print "Sending the: " + str(j) + " package"
  # Para enviar todo el paquete por linea
  for i in range(0,99):
    msg = str(y[i]) + "," + str(y[i]*2) + "," + str(y[i]*0.5) + "," + str(y[i]*10)
    ser.write(msg + '\n')								# Enviar una linea al puerto serial Formato: 0.001,0.002,0.003,1  (x,y,z,f)
    time.sleep(0.01)										# Espera de 10ms
  
print "Execution finished..."

 
