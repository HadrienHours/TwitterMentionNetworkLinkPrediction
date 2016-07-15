#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<filein.gz><fileout.gz>\e[0m\n"
    exit 1
fi

filein=$1
fileout=$2

zcat $filein | cut -d , -f3- | egrep -v ",[ ]*$" | sort -t , -k1,1 | gzip > $fileout
