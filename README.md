## Timelapse capture with Raspberry Pi in Python

### Overview:
The code in the file `capture.py` was created for the purpose of taking one picture
each second to get a real time measure of the movement of an object. This is designed
as a real-time system, working with threads and with
different optimizations in order to take as less as possible in the process of
saving the picture, so we can have a capture the closest possible to the real clock time,
so the photo will represent the second obtained. Everything is tested and developed in
the enviroment of a Raspberry Pi 3 Model B+, but it should work in any model that supports
the PiCamera and Python, and has more that one processor.

The rest of the files (`movementdetection.R` and `transfer.sh`) were created for
movement detection using edge detection and a BASH code to transfer the experiments
from the Raspberry Pi to our computer (using it as an Access Point to do a wireless
transference), but they are not described in this file (if you have questions about them
you can send me a PM).

### Configuration:

You can use both Python 2 and 3 to run the code, and after installing one of these,
you should install the following libraries: `twisted`, `PIL`, `picamera`, and maybe
others depending on the software you're using (it will be indicated on your terminal,
so follow the instructions there)

### Installing and running:

To run the program, you have to open a terminal in the same folder of the file, and
type the following command:

`$ python capture.py max_days timelapse experiment_name`

The first argument is the number of days that the experiment will save (it will
keep saving the photos but will override to keep that exact amount of days), the
second is the timelapse interval (in seconds), and the last one is the name that
will have the folder of the experiment (to transfer and process the data
after the capture).
