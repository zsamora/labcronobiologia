import os, sys, os.path, collections, picamera, gc, shutil, io, time, threading
from datetime import datetime, timedelta
from PIL import Image
from twisted.internet import task, reactor
from collections import deque

# Global variables
date_format = "%y_%m_%d_%H%M%S"
DIR = "/home/pi/Camera/Data/"
capt_time = None        # Capture time of the actual photo
N_FOLDERS = 0           # N of folders
TIMELAPSE = 1           # Time interval (in seconds)
FOLD = ""               # Actual folder
AUX = -1                # Actual photo second of the saving process
SEC = -1                # Actual photo second of the capture time
BUFFER = []             # Buffer of subfolders in Experiment
INDEX_DEL = 0           # Index for deletion of oldest directory
ERRORS = 0              # Cumulative errors
camera = picamera.PiCamera()
dates = deque([])       # Dates array for saving in threads
streams = deque([])     # Stream array for saving in threads

# Create a pool of image processors
done = False
pool = []
ThreadLock = threading.Lock()

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.capt_time = None
        self.picture = None
        self.start()

    def run(self):
        # This method runs in a separate thread
        global pool
        while not self.terminated:
            if self.event.wait(1):
                try:
                    global BUFFER
                    global INDEX_DEL
                    global ERRORS
                    global ThreadLock
                    global dates
                    global streams
                    self.stream.seek(0)
                    FOLD = self.capt_time[:-4]
                    SEC = int(self.capt_time[-2:])
                    AUX = int(datetime.now().strftime(date_format)[-2:])
                    if AUX > SEC:
                        ThreadLock.acquire()
                        ERRORS += AUX - SEC
                        ThreadLock.release()
                        print("(Error total: %s) Dia %s, a las %s:%s del intervalo de segundos [%s,%s]" %
                                (ERRORS, self.capt_time[0:8], self.capt_time[-6:-4],
                                self.capt_time[-4:-2], ((SEC + 1) % 60), AUX))
                    # The directory is not created
                    if not os.path.isdir(DIR + FOLD):
                        # Maximum size of folders, delete older
                        if len(BUFFER) == N_FOLDERS:
                            try:
                                shutil.rmtree(DIR + BUFFER[INDEX_DEL])
                                BUFFER[INDEX_DEL] = FOLD
                                INDEX_DEL = (INDEX_DEL + 1) % N_FOLDERS
                            except Exception as e:
                                print(e)
                        else:
                            BUFFER.append(FOLD)
                        # Create directory
                        try:
                            os.makedirs(DIR + FOLD)
                        except OSError:
                            raise
                    # Capture photo
                    try:
                        img = Image.open(self.picture)
                        img.save(DIR + FOLD +"/f" + self.capt_time + ".jpg")
                        print("saved",DIR + FOLD +"/f" + self.capt_time + ".jpg")
                        #AUX = SEC
                    except Exception as ex:
                        print(ex)
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    ThreadLock.acquire()
                    pool.append(self)
                    ThreadLock.release()

def captureLoop():
    global pool
    global ThreadLock
    global dates
    global streams
    try:
        ThreadLock.acquire()
        dates.append(datetime.now().strftime(date_format))
        s = io.BytesIO()
        camera.capture(s,"jpeg",use_video_port=True,quality=15,thumbnail=None,bayer=False)
        streams.append(s)
        ThreadLock.release()
        while (len(pool) != 0) and (len(streams) != 0):
            ThreadLock.acquire()
            processor = pool.pop()
            d = dates.popleft()
            s = streams.popleft()
            processor.capt_time = d
            processor.picture = s
            ThreadLock.release()
            processor.event.set()
    except Exception as e:
        print(e)



def main():
    global N_FOLDERS
    global TIMELAPSE
    global DIR
    global camera
    global BUFFER
    global pool
    if (len(sys.argv[1:]) != 3):
        print("Error de utilizacion: 'python capture.py",
                "max_days timelapse experiment_name'")
    else:
        TIMELAPSE = int(sys.argv[2])
        DIR = DIR + sys.argv[3] + "/"
        # Days* 24 hr + actual folder + latest folder (in progress)
        N_FOLDERS = int(sys.argv[1]) * 24 + 2
        # If the experiment folder exists
        if os.path.isdir(DIR):
            # Get folders ordered by name
            BUFFER = sorted(os.listdir(DIR))
        # If the number of folders > maximum folders, delete oldest
        if len(BUFFER) > N_FOLDERS:
            i = 0
            for i in range(len(BUFFER) - N_FOLDERS):
                shutil.rmtree(DIR + BUFFER[i])
            BUFFER = BUFFER[i+1:]
        # Deactivate automatic Garbage collector
        #gc.disable()
        pool = [ImageProcessor() for i in range (1)]
        # Initialize camera
        camera.resolution = (200, 200)
        camera.color_effects = (128, 128)
        camera.exposure_mode = 'sports'
        camera.framerate = 1
        # Wait 2 seconds, and until miliseconds is 0
        time.sleep(2+(100-int(datetime.now().strftime('%f')[:-4]))/100.0)
        print("Empezando la captura de fotografias del dia: %s" %
                (datetime.now().strftime(date_format)))
        # Set initial AUX
        # Call every TIMELAPSE seconds
        task.LoopingCall(captureLoop).start(TIMELAPSE)
        reactor.run()

if __name__ == '__main__':
    main()

# Shut down the processors in an orderly fashion
while pool:
    with ThreadLock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
