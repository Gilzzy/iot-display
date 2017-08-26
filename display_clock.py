import pifacecad
import datetime
import time
import serial
import csv
import os

cad = pifacecad.PiFaceCAD()
cad.lcd.clear()
cad.lcd.backlight_on()
cad.lcd.blink_off()

ser = serial.Serial(
	'/dev/ttyUSB0',
	baudrate = 57600,
	parity=serial.PARITY_NONE,
	#stopbits=serial.STOPBITS_NONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

file = open("/home/pi/data_log.csv", "a")
i=0
if os.stat("/home/pi/data_log.csv").st_size == 0:
        file.write("Time,Sensor1,Sensor2,Sensor3,Sensor4,Sensor5\n")

count = 1

if ser.isOpen():
    ser.close()
ser.open()
ser.isOpen()

ser.flushInput()
ser.flushOutput()

while (count > 0):
	message = str(ser.readline(),'ascii')
	time.sleep(.1)
	#ser.flushInput()
	print(message)
	cad.lcd.home()
	date = datetime.datetime.now()
	cad.lcd.cursor_on()
	cad.lcd.write(date.strftime("Time: %H:%M:%S"))
	cad.lcd.set_cursor(0, 1)
	cad.lcd.write(message)
	cad.lcd.cursor_off()
	

	file.write(str(date)+","+str(message)+"\n")
	file.flush()
	time.sleep(5)

