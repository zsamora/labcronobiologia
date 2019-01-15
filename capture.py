import time, os, sys, os.path, collections, picamera, gc, shutil, io, threading
from datetime import datetime, timedelta
from picamera import PiCamera
from twisted.internet import task, reactor
from PIL import Image

# Global variables
date_format = "%y_%m_%d_%H%M%S"
DIR = "/home/pi/Camera/Data/"
capt_time = None # Capture time of the actual photo
N_FOLDERS = 0    # N of folders
TIMELAPSE = 1    # Time interval (in seconds)
FOLD = ""        # Actual folder
AUX = -1         # Previous photo second (detection of errors)
SEC = -1         # Actual photo second
BUFFER = []      # Buffer of subfolders in Experiment
INDEX_DEL = 0    # Index for deletion of oldest directory
ERRORS = 0       # Cumulative errors
camera = picamera.PiCamera()

lock = threading.Lock()
pool = []

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start() # Empieza un thread y llama a run()

    def run(self):
        while not self.terminated:
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    capt_time = datetime.now().strftime(date_format)
                    img = Image.open(self.stream)
                    img.save("f" + capt_time + ".jpg")
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    with lock:
        processor = pool.pop()
    yield processor.stream
    processor.event.set()

def captureLoop():
    global capt_time
    global AUX
    global SEC
    global FOLD
    global BUFFER
    global INDEX_DEL
    global ERRORS
    capt_time = datetime.now().strftime(date_format)
    FOLD = capt_time[:-4]
    SEC = int(capt_time[-2:])
    # Actual photo is not the next expected photo
    if (SEC - (AUX + 1)) % 60 != 0:
        ERRORS += (SEC - (AUX + 1)) % 60
        print("(Error total: %s) Dia %s, a las %s:%s del intervalo de segundos [%s,%s]" %
                (ERRORS, capt_time[0:8], capt_time[-6:-4],
                capt_time[-4:-2], ((AUX + 1) % 60), ((SEC - 1) % 60)))
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
        camera.capture(DIR + FOLD +"/f" + capt_time + ".jpg",
            use_video_port=True,quality=15,thumbnail=None,bayer=False)
        AUX = SEC
        # Collect garbage
        #gc.collect()
    except Exception as ex:
        print(ex)

def main():
    global N_FOLDERS
    global TIMELAPSE
    global DIR
    global camera
    global AUX
    global BUFFER
    global pool
    global lock
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
        pool = [ImageProcessor() for i in range (4)]
        # Initialize camera
        camera.resolution = (200, 200)
        #camera.framerate = 1
        camera.color_effects = (128, 128)
        camera.exposure_mode = 'sports'
        camera.iso = 100
        #camera.start_preview()
        # Wait 2 seconds, and until miliseconds is 0
        time.sleep(2+(100-int(datetime.now().strftime('%f')[:-4]))/100.0)
        print("Empezando la captura de fotografias del dia: %s" %
                (datetime.now().strftime(date_format)))
        # Set initial AUX
        AUX = int(datetime.now().strftime('%S'))-1
        camera.capture_sequence(streams(), use_video_port=True)
        # Call every TIMELAPSE seconds
        #task.LoopingCall(captureLoop).start(TIMELAPSE)
        #reactor.run()


if __name__ == '__main__':
    main()
