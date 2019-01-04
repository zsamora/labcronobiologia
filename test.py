import time
import threading
import os
from datetime import datetime
from twisted.internet import task, reactor


starttime = time.time()
timeout = 1.0 # Sixty seconds
def printTime():
	print(datetime.now().strftime('%M:%S.%f')[:-4])
	# Creación del directorio con captura de error
	if not os.path.exists(directory):
    	try:
	    	os.makedirs(directory)
		except OSError as e:
	    	if e.errno != errno.EEXIST:
	        	raise

t = int(datetime.now().strftime('%f')[:-4])
delay = (99-t)/100.0
time.sleep(2+delay)
l = task.LoopingCall(printTime)
l.start(timeout) # call every  1 seconds
reactor.run()
