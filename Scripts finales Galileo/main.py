# Importar la libreria 
import serial
from scipy.signal import medfilt
from scipy.signal import wiener


# Configurar el puerto serial
ser = serial.Serial('/dev/tnt0', 9600)

# Constantes
nData = 100													# Cantidad de datos para muestreo  <----- SE PUEDE MODIFICAR

# Variables globales
Xarreglo = []
Yarreglo = []
Zarreglo = []
Farreglo = []


# Maquina de estados - Rutina principal
ctr = 0																# Este es el contador de los datos insertados		
while True:
  #----------------------------------------------------------------------------------------
  # Estado de WAIT
  msg = ser.readline()								# El readline() espera hasta que llegue un dato
  #----------------------------------------------------------------------------------------
  # Estado de APPEND
  append(msg)													# Invocar la subrutina append
  ctr = ctr + 1												# Incrementar los valores insertados
  if(ctr == 100):		
	#----------------------------------------------------------------------------------------
  # Estado de FILTER
    filtro()													# En caso de llegar a los 100 elementos
  #----------------------------------------------------------------------------------------
  # Estado de HYSTHERESIS
  	hystheresis()
  #----------------------------------------------------------------------------------------
  # Estado de CLEAR
  	ctr = 0
    Xarreglo = []
    Yarreglo = []
    Zarreglo = []
    Farreglo = []
  
  
# Funciones

def append(msg):
  msg.split(",")
  Xarreglo.append(float(msg[0]))
  Yarreglo.append(float(msg[1]))
  Zarreglo.append(float(msg[2]))
  Farreglo.append(float(msg[3]))

def filtro():
  
  Xarreglo = medfilt(Xarreglo,21)
  Yarreglo = medfilt(Yarreglo,21)
  Zarreglo = medfilt(Zarreglo,21)
  Farreglo = medfilt(Farreglo,21)
  
  Xarreglo = wiener(Xarreglo,11)
  Yarreglo = wiener(Yarreglo,11)
  Zarreglo = wiener(Zarreglo,11)
  Farreglo = wiener(Farreglo,11)
  
  
  



