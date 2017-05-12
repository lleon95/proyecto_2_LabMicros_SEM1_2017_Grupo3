# Importar librerias
import serial
import pyautogui

# Preparar el puerto serial
#SP = input("Puerto serial: ")
#BR = input("Baudrate: ")
#USB = serial.Serial(SP,BR)
USB = serial.Serial('/dev/ttyACM2',9600)

# Variables globales
R_button = 0
L_button = 0
x_pos = 300
y_pos = 300

# Rutina principal
msg = USB.readline()
msg = USB.readline()
while True:
  # Leer el puerto serial
  msg = USB.readline()
  #print msg
  # Desempaquetar datos
  msg = msg.split(',')
  x = float(msg[0])
  y = float(msg[1])
  LB = float(msg[2])
  RB = float(msg[3])
  # Arreglando a pantalla
  x = (x/10)*100
  y = (y/10)*100
  x_pos = x_pos + x
  y_pos = y_pos + y
  # Desplazamiento
  if x != 0 or y != 0:
      pyautogui.moveTo(x_pos,y_pos)
  # Clicks
  #	Click Derecho
  	# Si se presiona el boton derecho
  if(R_button == 0 and RB == 1):
    pyautogui.rightClick()
    R_button = RB
    # Si se suelta el boton derecho
  elif(R_button == 1 and RB == 0):
    R_button = RB
  # Click Izquierdo
  	# Si se presiona el boton izq
  if(L_button == 0 and LB == 1):
    pyautogui.mouseDown()
    L_button = LB
    # Soltar el boton izquierdo
  elif(L_button == 1 and LB == 0):
    pyautogui.mouseUp()
    L_button = LB


#pyautogui.mouseDown(); pyautogui.mouseUp()  # does the same thing as a left-button mouse click
#pyautogui.mouseDown(button='right')  # press the right button down
#pyautogui.mouseUp(button='right', x=100, y=200)  # move the mouse to 100, 200, then release the right button up.

# Formato del lado de Galileo:
# USB.write(str(x)+','+str(y)+','+str(LB)+','+str(RB)+','+'\n')
#pyautogui.moveTo(100, 100, 2, pyautogui.easeInQuad)     # start slow, end fast
