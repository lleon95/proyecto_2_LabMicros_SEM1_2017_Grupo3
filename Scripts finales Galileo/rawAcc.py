# Este codigo no contempla filtros; solo considera condiciones.

# Importar la libreria
import serial

# Alistar puertos seriales
PC = serial.Serial('/dev/ttyGS0',9600)  # Para el PC, conectado al OTG
BT = serial.Serial('/dev/ttyS0',9600)   # Desde el acelerometro por BT o conexion par

# Quitar basura
BT.readline()
BT.readline()

# Variables globales
x = 0
y = 0
x_acc = 0
y_acc = 0

# Rutina principal
while True:
    # Recibir el dato
    msg = BT.readline()
    # Desempaquetar el mensaje
    msg = msg.split(',')
    # Hacer un try para evitar errores de ejecucion
    try:
        # Aqui puede retornar error
        if float(msg[0]) > -10 and float(msg[0]) < 10 and float(msg[1]) > -10 and float(msg[1]):
            # Valor del acelerometro
            x_acc = msg[0]
            y_acc = msg[1]
            # Valor final - x
            if x_acc > 0.5:
                x = 1
            elif x_acc < -0.5:
                x = -1
            else
                x = 0
            # Valor final - y
            if y_acc > 0.5:
                y = 1
            elif y_acc < -0.5:
                y = -1
            else
                y = 0
            # Enviar los datos al serial
            PC.write(str(x) + ',' + str(y) + ',' + '0' + ',' + '0' + ',' +'\n')
