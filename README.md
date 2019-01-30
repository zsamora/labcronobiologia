## Timelapse capture with Raspberry Pi in Python

### Overview:
The code in the file `capture.py` was created for the purpose of taking one picture
each second to get a real time measure of movement of an object. This is planned
as a system that works like a real-time system, working with threads and with
different optimizations in order to take as less as possible in the process of
saving the picture, and in having a picture the closest we can (with this hardware
and software) to the real time (the photo really represents the second obtained).

The rest of the files (`movementdetection.R` and `transfer.sh`) were created for
movement detection using edge detection and a BASH code to transfer the experiments
from the Raspberry Pi to our computer (using it as an Access Point), but they are
not described in this file (if you have questions you can send me a PM)

### Configuration:

You can use both Python 2 and 3 to run the code, and after installing one of these,
you should install the following libraries: `twisted`, `PIL`, `picamera`, and maybe
others depending on the software you're using (it will appeared on your terminal)

### Installing and running:

To run the program, you have to open a terminal in the same folder of the file, and
type the following command:

`$ python capture.py max_days timelapse experiment_name`

The first argument is the number of days that the experiment will save (it will
keep saving the photos but will override to keep that exact amount of days), the
second is the timelapse interval (in seconds), and the last one is the name that
will have the folder of the experiment (to transfer and process after the capture).

### Credits
