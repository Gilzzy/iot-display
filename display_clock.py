#!/usr/bin/env python3
import _thread
import threading
import time
import pifacecad
import datetime
import serial
import csv
import os

dataArray = []
threads = []

dataArrayLock = None
screenLock = None

cad = pifacecad.PiFaceCAD()
cad.lcd.clear()
cad.lcd.backlight_on()
cad.lcd.blink_off()

class AbstractThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.tick = 1
		threads.append(self)
	def run(self):
		while 1:
			self.execute()
			time.sleep(self.tick)

class DisplayThread(AbstractThread):
	def __init__(self, displayType):
		self.index = -1
		self.displayType = displayType
		if (self.displayType == 2):
			self.tick = 0
		else:
			self.tick = 0.2
		AbstractThread.__init__(self)
		
	def lcd_message(self, x, y, message):
		screenLock.acquire()
		cad.lcd.cursor_on()
		cad.lcd.set_cursor(x, y)
		cad.lcd.write(message)
		cad.lcd.cursor_off()
		screenLock.release()

	def execute(self):
		if (self.displayType == 1):
			date = datetime.datetime.now()
			self.lcd_message(0, 0, date.strftime("Time: %H:%M:%S"))
		else:
			message = None
			dataArrayLock.acquire()
			newLength = len(dataArray) - 1
			if(newLength > self.index):
				self.index = newLength - 1
				message = dataArray[-1]
			dataArrayLock.release()
			
			if (message != None):
				self.lcd_message(0, 1, message)
			

			
class ReadThread(AbstractThread):
	def __init__(self):
		self.tick = 0.1
	
		self.device = serial.Serial(
			'/dev/ttyUSB0',
			baudrate = 57600,
			parity=serial.PARITY_NONE,
			#stopbits=serial.STOPBITS_NONE,
			bytesize=serial.EIGHTBITS,
			timeout=1
		)

		if self.device.isOpen():
			self.device.close()

		self.device.open()
		self.device.isOpen()
		
		self.device.flushInput()
		self.device.flushOutput()
		
		AbstractThread.__init__(self)
	def execute(self):
		
		message = str(self.device.readline(),'ascii').strip(chr(0))
		
		b = bytearray()
		b.extend(map(ord, message))
		print(b)

		if (len(message)>0):
			self.device.flushOutput()
			self.device.flushInput()
			dataArrayLock.acquire()
			dataArray.append(message)
			dataArrayLock.release()
			
			


class WriteThread(AbstractThread):
	def __init__(self):
		self.tick = 0
		self.index = -1
		self.file = open("/home/pi/data_log.csv", "a")
		if os.stat("/home/pi/data_log.csv").st_size == 0:
		        self.file.write("Time,Sensor1,Sensor2,Sensor3,Sensor4,Sensor5\n")
		AbstractThread.__init__(self)
	def execute(self):
		date = datetime.datetime.now()
		dataArrayLock.acquire()
		newLength = len(dataArray) - 1
		while self.index < newLength:
			message = dataArray[self.index]
			# write to file
			print("Writing {} to file".format(message))
			self.file.write(str(date)+","+str(message)+"\n")
			self.file.flush()
			self.index += 1
			
		dataArrayLock.release()

		
		
		
## To create a "worker" (thread)
# Copy this class:

class MyNewThread (AbstractThread):
	# class constructor
	def __init__(self, threadID, name):
		# thread sleep time (seconds), longer = less priority
		self.tick = 1
		
		AbstractThread.__init__(self, threadID, name)
		
	def execute(self):
		# your code logic here.
		# try to avoid while loops
		print("My New Thread")
		
dataArrayLock = threading.Lock()
screenLock = threading.Lock()

displayThread  = DisplayThread(1)
displayThread2 = DisplayThread(2)
readThread     = ReadThread()
writeThread    = WriteThread()

for thread in threads:
	thread.start()
	
for thread in threads:
	thread.join()
	
