#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<filein><fileout>\e[0m\n"
    echo -e "Format filein:\t\e[3mts,userId,hashtag,listWords\e[0m"
    exit 1
fi

filein=$1
fileout=$2

zcat $filein | cut -d , -f2-3 | sort | uniq | sort -t , -k1,1 | gzip > $fileout
