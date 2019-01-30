## Timelapse capture with Raspberry Pi in Python

### Overview:

The code in the file `capture.py` was created for the purpose of taking one picture
each second (or any timelapse) to get a real time measure of the movement
of an object. This was designed as a real-time system, working with threads and with
different optimizations so we can have a capture as close as possible to the real clock time,
so the photo will really represent the second recorded. Everything is tested and developed in
the enviroment of a Raspberry Pi 3 Model B+, but it should work in any model that supports
the PiCamera and Python, and has more that one processor.

The idea of this project is to have a stable capture camera to record long periods of time
(1 month or more) that is also simple to manipulate and edit, cheap to build on your own, and
extensible to new tools you want to work with.

The rest of the files (`movementdetection.R` and `transfer.sh`) were created for
movement detection using edge detection and a BASH code to transfer the experiments
from the Raspberry Pi to our computer (using it as an Access Point to make wireless
transference), but they are not described in this file. If you have questions about them
you can send me a PM.

### Configuration:

You can use both Python 2 and 3 to run the code, and after installing one of these,
you have to install the following libraries: `twisted`, `PIL`, `picamera`, and maybe
others depending on the software you're using (it will be indicated on your terminal
when you run the program, so follow the instructions in there)

### Installing and running:

To execute the program, you have to open a terminal in the same folder of this file,
and type the following command:

`$ python capture.py max_days timelapse experiment_name`

The first argument is the number of days that the experiment will save (it will
keep saving the photos but will override the folders to keep that exact amount of days),
the second is the timelapse interval (in seconds), and the last one is the name that
will have the folder of the experiment (to transfer and process the data after the capture).

### Design and tests:

In the process of developing we have tested differents settings, obtaining the best results
principally with the combination of two methods:

* Using the command `nice -5 python ...`
* Parallelize the process of capture and save

The idea was to give some priority to this program, in order to have the CPU using most
of his power in the capture process, and also, working with the different cores of the
processor so the saving process (which takes longer than the capture process), will
have place in another thread and will reduce the number of errors. The results are
pretty good with a rate of 5 photos lost per hour, with 1 second timelapse.

### Credits and license:

This work took place in 2019, and is licensed under GNU General Public License (GPLv3). It was inspired
by the following links, so we hope you can re-use it, and comment us on any idea
or problem that you found that could improve it.
