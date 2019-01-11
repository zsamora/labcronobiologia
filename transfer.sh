#!/bin/bash
if [ -z "$1" ]; then
  echo "Transferencia de todos los experimentos"
else
  EXP_NAME=$1
  echo "Transferencia de "$EXP_NAME
fi
TMP=$(mktemp)
time (nice -10 rsync -r pi@192.168.4.1:/home/pi/Camera/Data/$EXP_NAME . ) 2>$TMP
awk -F'[ ms]+' '/^real/ {print "copy time: "1000*$2"ms"}' $TMP
rm $TMP
