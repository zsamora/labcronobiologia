import time
import threading
from datetime import datetime
from twisted.internet import task, reactor


starttime = time.time()
timeout = 1.0 # Sixty seconds
def printTime():
	print(datetime.now().strftime('%M:%S.%f')[:-4])

t = int(datetime.now().strftime('%f')[:-4])
delay = (99-t)/100.0
time.sleep(2+delay)
l = task.LoopingCall(printTime)
l.start(timeout) # call every  1 seconds
reactor.run()
