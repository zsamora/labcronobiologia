import time, picamera, os
from datetime import datetime
from twisted.internet import task, reactor

camera = picamera.PiCamera()
camera.resolution = (800, 600)
camera.color_effects = (128, 128)
camera.exposure_mode = 'sports'
timeout = 1.0 # Sixty seconds

def printTime():
    capt_time = datetime.now().strftime('%y_%m_%d_%H%M%S')
    fold_time = capt_time[:-4]
    filename = "f" + capt_time + ".jpg"
    directory = "/home/pi/Camera/Data/" + fold_time +"/"
    #print(directory)
    try:
        os.makedirs(directory)
    except OSError:
        if not os.path.isdir(directory):
            raise
    try:
        camera.capture(directory+filename,use_video_port=True,quality=15,thumbnail=None,bayer=False)
#        print("Saved " + capt_time)
    except Exception as ex:
           print(ex)
t = int(datetime.now().strftime('%f')[:-4])
delay = (100-t)/100.0
time.sleep(2+delay)
print("Starting captures")
l = task.LoopingCall(printTime)
l.start(timeout) # call every  1 seconds
reactor.run()

