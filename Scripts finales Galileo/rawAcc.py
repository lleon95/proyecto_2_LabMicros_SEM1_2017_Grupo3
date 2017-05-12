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
    print msg
    msg = msg.split(',')
    # Hacer un try para evitar errores de ejecucion
    try:
        # Aqui puede retornar error
        if float(msg[0]) > -10 and float(msg[0]) < 10 and float(msg[1]) > -10 and float(msg[1]):
            # Valor del acelerometro
            x_acc = float(msg[0])
            y_acc = float(msg[1])
            # Valor final - x
            if x_acc > 0.5:
                x_acc = (x_acc - 0.5)/0.5   # Cantidad de desplazamiento
                x = x_acc * 10              # Maximo de desplazamiento
            elif x_acc < -0.5:
                x_acc = (x_acc + 0.5)/0.5   # Cantidad de desplazamiento
                x = x_acc * 10              # Maximo de desplazamiento
            else:
                x = 0
            # Valor final - y
            if y_acc > 0.5:
                y_acc = (y_acc - 0.5)/0.5   # Cantidad de desplazamiento
                y = y_acc * 10              # Maximo de desplazamiento
            elif y_acc < -0.5:
                y_acc = (y_acc + 0.5)/0.5   # Cantidad de desplazamiento
                y = y_acc * 10              # Maximo de desplazamiento
            else:
                y = 0
            # Enviar los datos al serial
            PC.write(str(x) + ',' + str(y) + ',' + '0' + ',' + '0' + ',' +'\n')
    except:
        print "Dato invalido recibido"
