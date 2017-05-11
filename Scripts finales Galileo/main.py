# Importar la libreria 
import serial
from scipy.signal import medfilt
from scipy.signal import wiener
import time

# Configurar el puerto serial
BT = serial.Serial('/dev/tnt0', 9600)
USB = serial.Serial('/dev/ttyS1', 9600)

# Constantes
nData = 100                         # Cantidad de datos para muestreo  <----- SE PUEDE MODIFICAR

# Variables globales
Xarreglo = []
Yarreglo = []
Zarreglo = []
Farreglo = []
x = 0
y = 0
LB = 0
RB = 0


# Maquina de estados - Rutina principal
start_time = time.time()
ctr = 0                               # Este es el contador de los datos insertados   
while True:
  #----------------------------------------------------------------------------------------
  # Estado de WAIT
  msg = BT.readline()               # El readline() espera hasta que llegue un dato
  #----------------------------------------------------------------------------------------
  # Estado de APPEND
  append(msg)                         # Invocar la subrutina append
  ctr = ctr + 1                       # Incrementar los valores insertados
  if(ctr == 100):   
  #----------------------------------------------------------------------------------------
  # Estado de FILTER
    filtro()                          # En caso de llegar a los 100 elementos
  #----------------------------------------------------------------------------------------
  # Estado de ANALISIS
    analisis()
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
  
def analisis():
  for j in range(0,99):
    if ((Xarreglo[j]<0.4)and(Xarreglo[j]>-0.4)):
      x = 0
    elif (Xarreglo[j]>0.6):
      x = 1
    elif (Xarreglo[j]<-0.6):
      x = -1
    
    if ((Yarreglo[j]<0.4)and(Yarreglo[j]>-0.4)):
      y = 0
    elif (Yarreglo[j]>0.6):
      y = 1
    elif (Yarreglo[j]<-0.6):
      y = -1
          
    if (Farreglo[j]<3.2):
      flex = 0
    elif (Farreglo[j]>3.4):
      flex = 1
        
    dx = abs(Xarreglo[j]-0.5)
    dy = abs(Yarreglo[j]-0.5)
    x = int(round(x*dx*6.6))
    y = int(round(y*dy*6.6))
    LB = flex
    RB = 0
    
    elapsed_time = time.time() - start_time
    if (x==0 and y==0 and flex==1):
      if (elapsed_time>1.5):
        LB = 0
        RB = 1
      #else: Supongo que esta vacio
    else:
      start_time = time.time()
    
    sendtoPC(x,y,LB,RB)

# Funcion para enviar desplazamiento en relativo (Ej: 1px)
def sendtoPC(x,y,LB,RB):
  # Documentacion: 
    # Si x > 0: derecha
    # Si x < 0: izquierda
    # Si y > 0: abajo
    # Si y < 0: arriba
    # LB: Left Button: 0: soltar, 1: presionar
    # RB: Right Button: 0: soltar, 1: presionar
  # Para enviar al PC
  USB.write(str(x)+','+str(y)+','+str(LB)+','+str(RB)+','+',\n')
            
  
  
  
  


