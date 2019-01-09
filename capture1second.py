import time, picamera, os, sys, os.path
from datetime import datetime, timedelta
#from threading import Timer
from twisted.internet import task, reactor

# Global variables
date_format = "%y_%m_%d_%H%M%S"
DIR = "/home/pi/Camera/Data/"
capt_time = None # Capture time
DAYS = 15        # N of days
N_FOLDERS = 0    # N of folders
TIMELAPSE = 1    # Time interval (in seconds)
AUX = -1         # Auxiliar variable for counting missing pictures
SEC = -1         # Second corresponding to actual photo

def captureLoop():
    global capt_time
    global AUX
    global SEC
    global N_FOLDERS
    capt_time = datetime.now().strftime(date_format)
    SEC = int(capt_time[-2:])
    if SEC < AUX:
        SEC += 60
    if SEC - AUX != 1:
        print("Error en el dia "+capt_time[0:7]+", a las " + capt_time[10:13]+":"+capt_time[-4:-2]+ " del segundo", ((AUX + 1) % 60), "al segundo ", ((SEC - 1) % 60))
    try:
        os.makedirs(DIR + capt_time[:-4] +"/")
        N_FOLDERS -= 1
    except OSError:
        if not os.path.isdir(DIR + capt_time[:-4] +"/"):
            raise
    try:
        camera.capture(DIR + capt_time[:-4] +"/"+"f" + capt_time + ".jpg",use_video_port=True,quality=15,thumbnail=None,bayer=False)
        AUX = SEC
        # print("Saved " + capt_time)
    except Exception as ex:
        print(ex)

def main():
    global DAYS
    global N_FOLDERS
    global TIMELAPSE
    global DIR
    if (len(sys.argv[1:]) != 3):
        print("Error de utilizacion: 'python capture1second.py days timelapse experiment_name'")
    else:
        now = datetime.now()
        DAYS = int(sys.argv[1])
        TIMELAPSE = int(sys.argv[2])
        DIR = DIR + sys.argv[3]
        N_FOLDERS = DAYS * 24 + 2
        # Initialize camera
        camera = picamera.PiCamera()
        camera.resolution = (200, 200)
        camera.color_effects = (128, 128)
        camera.exposure_mode = 'sports'
        # Wait 2 seconds, and until miliseconds is 0
        time.sleep(2+(100-int(datetime.now().strftime('%f')[:-4]))/100.0)
        print("Starting captures")
        # Call every TIMELAPSE seconds
        task.LoopingCall(captureLoop).start(TIMELAPSE)
        reactor.run()
        while FOLDERS != 0:
            continue
        reactor.stop()

if __name__ == '__main__':
    main()
