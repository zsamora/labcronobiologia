TMP=$(mktemp)
time (nice -0 rsync -r pi@192.168.4.1:/home/pi/Camera/Data/19_01_04_14/ . ) 2>$TMP
awk -F'[ ms]+' '/^real/ {print "copy time: "1000*$2"ms"}' $TMP
rm $TMP
rm f19_01_04_14*
