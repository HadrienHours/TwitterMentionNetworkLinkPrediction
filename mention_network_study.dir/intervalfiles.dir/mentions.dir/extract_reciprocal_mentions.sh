#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<fileinput.gz><fileoutput.gz>\e[0m\n"
    exit 1
fi

filein=$1
fileout=$2

zcat $filein | sort | uniq | cut -d , -f1-2 | sort | uniq -c | awk '{if($1>=2){print $2}}' | gzip > $fileout
