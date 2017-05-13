# Importar la libreria
import serial
import numpy as np
import time

# Configurar el puerto serial
USB = serial.Serial('/dev/tnt1', 115200)
BT = serial.Serial('/dev/ttyACM0', 9600)

# Constantes
nData = 10                         # Cantidad de datos para muestreo  <----- SE PUEDE MODIFICAR

# Variables globales
X_raw_arreglo = []
Y_raw_arreglo = []
Z_raw_arreglo = []
F_raw_arreglo = []
Xarreglo = []
Yarreglo = []
Zarreglo = []
Farreglo = []

# x = 0
# y = 0
# LB = 0
# RB = 0
startCounter = 0


# Funciones

def agregar(msg):
  global X_raw_arreglo, Y_raw_arreglo, Z_raw_arreglo, F_raw_arreglo
  msg = msg.split(",")
  #print msg
  try:
    if float(msg[0]) < 10 and float(msg[1]) < 10 and float(msg[2]) < 10:
      X_raw_arreglo.append(float(msg[0]))
      Y_raw_arreglo.append(float(msg[1]))
      #Z_raw_arreglo.append(float(msg[2]))
      #Farreglo.append(float(msg[3]))
      F_raw_arreglo.append(0);
  except:
    print "Dato invalido recibido"

  return

def filtro():
  global X_raw_arreglo, Y_raw_arreglo, Z_raw_arreglo, F_raw_arreglo
  global Xarreglo, Yarreglo, Farreglo
  X_filtered_arreglo = medfilt(X_raw_arreglo,11)
  Y_filtered_arreglo = medfilt(Y_raw_arreglo,11)
  #Z_filtered_arreglo = medfilt(Z_raw_arreglo,11)
  F_filtered_arreglo = medfilt(F_raw_arreglo,11)

  # Anotacion importante - Wiener no puede contener 0's

  # Deben declararse globales


  # Xarreglo = wiener(X_filtered_arreglo,11)
  # Yarreglo = wiener(Y_filtered_arreglo,11)
  # Zarreglo = wiener(Z_filtered_arreglo,11)
  Xarreglo = X_filtered_arreglo
  Yarreglo = Y_filtered_arreglo
  #Zarreglo = Z_filtered_arreglo
  #Farreglo = wiener(F_filtered_arreglo,11)
  Farreglo = F_filtered_arreglo
  return

# Funcion para enviar desplazamiento en relativo (Ej: 1px)
def sendtoPC(x_out,y_out,LB_out,RB_out):
  # Documentacion:
    # Si x > 0: derecha
    # Si x < 0: izquierda
    # Si y > 0: abajo
    # Si y < 0: arriba
    # LB: Left Button: 0: soltar, 1: presionar
    # RB: Right Button: 0: soltar, 1: presionar
  # Para enviar al PC
  USB.write(str(x_out)+','+str(y_out)+','+str(LB_out)+','+str(RB_out)+','+',\n')
  return

def analisis():

  global Xarreglo, Yarreglo, Farreglo
  start_time = 0
  x = 0
  y = 0
  flex = 0
  print Xarreglo
  for j in range(0,len(Xarreglo)):
    print j

    if ((Xarreglo[j]<0.49)and(Xarreglo[j]>-0.49)):
      x = 0
    elif (Xarreglo[j]>0.51):
      #x = 1
      x = 1
    elif (Xarreglo[j]<-0.51):
      #x = -1
      x = -1

    if ((Yarreglo[j]<0.49)and(Yarreglo[j]>-0.49)):
      y = 0
    elif (Yarreglo[j]>0.51):
      #y = 1
      y = 1
    elif (Yarreglo[j]<-0.51):
      #y = -1
      y = -1

    if (Farreglo[j]<3.2):
      flex = 0
    elif (Farreglo[j]>3.4):
      flex = 1


    #dx = abs(Xarreglo[j]-0.5)
    #dy = abs(Yarreglo[j]-0.5)
    #x = int(round(x*dx*6.6))
    #y = int(round(y*dy*6.6))
    #x = x*5
    #y = y*5
    LB = flex
    RB = 0
    time.sleep(0.01)
    sendtoPC(x,y,LB,RB)

    # elapsed_time = time.time() - start_time
    # if (x==0 and y==0 and flex==1):
    #   if (elapsed_time>1.5):
    #     LB = 0
    #     RB = 1
    #   #else: Supongo que esta vacio
    # else:
    #   start_time = time.time()

  return

def clear_list():
  global X_raw_arreglo, Y_raw_arreglo, Z_raw_arreglo, F_raw_arreglo
  X_raw_arreglo = []
  Y_raw_arreglo = []
  Z_raw_arreglo = []
  F_raw_arreglo = []
  return


# Maquina de estados - Rutina principal
start_time = time.time()
ctr = 0                              # Este es el contador de los datos insertados
BT.readline()
BT.readline()
while True:
  #----------------------------------------------------------------------------------------
  # Estado de WAIT
  msg = BT.readline()               # El readline() espera hasta que llegue un dato
  BT.write('1\n')
  #----------------------------------------------------------------------------------------
  # Estado de APPEND
  agregar(msg)                         # Invocar la subrutina append
  print msg
  ctr = ctr + 1                       # Incrementar los valores insertados

  if(ctr == nData):
  #----------------------------------------------------------------------------------------
  # Estado de FILTER
    filtro()                          # En caso de llegar a los 100 elementos
  #----------------------------------------------------------------------------------------
  # Estado de ANALISIS
    analisis()
  #----------------------------------------------------------------------------------------
  # Estado de CLEAR
    ctr = 0
    clear_list()
