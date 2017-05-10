# Importar librerias
import serial
import pyautogui

# Preparar el puerto serial
SP = input("Puerto serial: ")
BR = input("Baudrate: ")
USB = serial.Serial(SP,BR)

# Variables globales
R_button = 0
L_button = 0

# Rutina principal
while True:
  # Leer el puerto serial
  msg = USB.readline()
  # Desempaquetar datos
  msg = msg.split(',')
  x = float(msg[0])
  y = float(msg[1])
  LB = float(msg[2])
  RB = float(msg[3])
  # Desplazamiento
  pyautogui.moveRel(x,y)
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