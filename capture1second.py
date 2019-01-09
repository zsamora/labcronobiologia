import time, os, sys, os.path, collections, picamera
from datetime import datetime, timedelta
from picamera import PiCamera
from twisted.internet import task, reactor

# Global variables
date_format = "%y_%m_%d_%H%M%S"
DIR = "/home/pi/Camera/Data/"
capt_time = None # Capture time of the actual photo
N_FOLDERS = 0    # N of folders
TIMELAPSE = 1    # Time interval (in seconds)
FOLD = ""        # Actual folder
AUX = -1         # Auxiliar variable for counting missing pictures
SEC = -1         # Second corresponding to actual photo
BUFFER = []      # Buffer for maximum amount of subfolders in Experiment
INDEX_DEL = 0    # Index for deletion of older directory
camera = picamera.PiCamera()

def captureLoop():
    global capt_time
    global AUX
    global SEC
    global FOLD
    global BUFFER
    global INDEX_DEL
    capt_time = datetime.now().strftime(date_format)
    FOLD = capt_time[:-4]
    SEC = int(capt_time[-2:])
    # Actual photo is not the next photo expected
    if ((AUX + 1) % 60) != SEC:
        print("Error en el dia %s, a las %s:%s, fotos perdidas del segundo %s al %s" % (capt_time[0:8],capt_time[-6:-4],capt_time[-4:-2],((AUX + 1) % 60),((SEC - 1) % 60)))
    # The directory is not created
    if not os.path.isdir(DIR + FOLD):
        # Maximum size of folders, delete older
        if len(BUFFER) == N_FOLDERS:
            os.rmdir(DIR + BUFFER[INDEX_DEL])
            BUFFER[INDEX_DEL] = FOLD
            INDEX_DEL = (INDEX_DEL + 1) % N_FOLDERS
        else:
            BUFFER.append(FOLD)
        # Create directory
        try:
            os.makedirs(DIR + FOLD)
        except OSError:
            raise
    # Capture photo
    try:
        camera.capture(DIR + FOLD +"/f" + capt_time + ".jpg",use_video_port=True,quality=15,thumbnail=None,bayer=False)
        AUX = SEC
        print("Objects collected:", gc.get_objects())
        gc.collect()
        # print("Saved " + capt_time)
    except Exception as ex:
        print(ex)

def main():
    global N_FOLDERS
    global TIMELAPSE
    global DIR
    global camera
    global AUX
    if (len(sys.argv[1:]) != 3):
        print("Error de utilizacion: 'python capture1second.py max_days timelapse experiment_name'")
    else:
        now = datetime.now()
        TIMELAPSE = int(sys.argv[2])
        DIR = DIR + sys.argv[3] + "/"
        N_FOLDERS = int(sys.argv[1]) + 1 # Days * 24 hr + actual folder
        if os.path.isdir(DIR):
            BUFFER = os.listdir(DIR).sort()
        # Deactivate automatic Garbage collector
        gc.disable()
        # Initialize camera
        camera.resolution = (200, 200)
        camera.color_effects = (128, 128)
        camera.exposure_mode = 'sports'
        # Wait 2 seconds, and until miliseconds is 0
        time.sleep(2+(100-int(datetime.now().strftime('%f')[:-4]))/100.0)
        print("Empezando la captura de fotografias: %s", datetime.now().strftime(date_format))
        # Set initial AUX
        AUX = int(datetime.now().strftime('%S'))-1
        # Call every TIMELAPSE seconds
        task.LoopingCall(captureLoop).start(TIMELAPSE)
        reactor.run()

if __name__ == '__main__':
    main()
