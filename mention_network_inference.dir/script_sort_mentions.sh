#!/bin/bash
NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<fileIn><fileOut>\e[0m\n"
    echo -e "File input format:\e[3m<uid,mid,direction,date>\e[0m"
    exit 1
fi

filein=$1
fileout=$2

#sort according to uid,mid,date
cat $filein | sort -g -t , -k1,1 -k2,2 -k4,4 > $fileout
