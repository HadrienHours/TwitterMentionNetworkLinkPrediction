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

#sort according to date,uid,mid
cat $filein | sort -g -t , -k3,3 -k1,1 -k2,2 > $fileout
