#!/usr/bin/env python3

import threading
import time

class SerialThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	
	def execute(self):
		while 1:
			time.sleep(1)
			print(self.name)
	
	def run(self):
		print ("Starting " + self.name)
		
		threadLock.acquire()
		self.execute()
		threadLock.release()

