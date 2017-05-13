# Importar la libreria
import serial
import numpy as np
import time

# Configurar el puerto serial
USB = serial.Serial('/dev/ttyGS0', 38400)
BT = serial.Serial('/dev/ttyS0', 38400)

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
            #Farreglo.append(float(msg[3]))
            F_raw_arreglo.append(0)
    except:
        print "Dato invalido recibido"

    return

def filtro():
    global X_raw_arreglo, Y_raw_arreglo, F_raw_arreglo
    global Xarreglo, Yarreglo, Farreglo
    # Generar el eje de abscisas
    X_axis = np.linspace(1,len(X_raw_arreglo),len(X_raw_arreglo))
    # Generar una matriz T de X
    A = np.vstack([X_axis, np.ones(len(X_axis))]).T
    # Adquirir la relacion m, b
    mx, bx = np.linalg.lstsq(A, np.array(X_raw_arreglo))[0]
    my, by = np.linalg.lstsq(A, np.array(Y_raw_arreglo))[0]
    # Generar la lista filtrada
    Xarreglo = np.dot(mx,X_axis) + bx
    Yarreglo = np.dot(my,X_axis) + by
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
    # Definicion de Histeresis
    minThreshold = 0.45
    maxThreshold = 0.55
    start_time = 0
    x = 0
    y = 0
    flex = 0
    for j in range(0,len(Xarreglo)):
        # Analisis para X
        if (Xarreglo[j]>minThreshold):
            dx = (Xarreglo[j] - minThreshold)/maxThreshold
            x += dx
        elif (Xarreglo[j]<-minThreshold):
            dx = (Xarreglo[j] + minThreshold)/maxThreshold
            x += dx
        else:
            x += 0
        # Analisis para y
        if (Yarreglo[j]>minThreshold):
            dy = (Yarreglo[j] - minThreshold)/maxThreshold
            y += dy
        elif (Yarreglo[j]<-minThreshold):
            dy = (Yarreglo[j] + minThreshold)/maxThreshold
            y += dy
        else:
            y += 0

    # Corregir X y Y
    x = round(x*10 / len(Xarreglo))
    y = round(y*10 / len(Xarreglo))
    # Enviar para corroborar
    sendtoPC(x,y,0,0)

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
    #print msg
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
