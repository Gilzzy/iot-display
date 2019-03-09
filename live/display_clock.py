import pifacecad
import datetime
import time
import serial
import csv
import os

from datetime import datetime
import subprocess

cad = pifacecad.PiFaceCAD()
cad.lcd.clear()
cad.lcd.backlight_on()
cad.lcd.blink_off()


count = 1
backlight = 1

time_alarm = str("06:30")
time_input = str("22:00")
#current_date = str("2019/02/18")

#time_alarm_test = datetime.strptime('%s %s'%(current_date, time_input),"%Y/%m/%d  %H:%M:%S")

while (count > 0):
	cad.lcd.home()
	date = datetime.now()
	cad.lcd.cursor_on()
	cad.lcd.set_cursor(5,0)
	cad.lcd.write(date.strftime("%H:%M"))
	cad.lcd.set_cursor(0,2)
	cad.lcd.write(date.strftime("%a %-d %b %Y"))
	cad.lcd.cursor_off()

#	print(time_alarm)
#	print(time_input)
#	print(date.strftime("%H:%M:%S"))

	if backlight == 0:
		if time_alarm == date.strftime("%H:%M"):
			cad.lcd.backlight_on()
			backlight = 1
	else :
		if time_input == date.strftime("%H:%M"):
			cad.lcd.backlight_off()
			backlight = 0

	if cad.switches[4].value:
		if backlight == 1:
			cad.lcd.backlight_off()
			backlight = 0
		else :
			cad.lcd.backlight_on()
			backlight = 1
	time.sleep(.5)

