#!/bin/bash
echo "Nombre del Experimento (vacio para transferir todos)"
read EXP_NAME
TMP=$(mktemp)
time (nice -10 rsync -r pi@192.168.4.1:/home/pi/Camera/Data/$EXP_NAME . ) 2>$TMP
awk -F'[ ms]+' '/^real/ {print "Tiempo de transferencia: "1000*$2"ms"}' $TMP
rm $TMP
