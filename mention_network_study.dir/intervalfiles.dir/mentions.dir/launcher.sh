#!/bin/bash

NARGS=4

if [ $# -ne $NARGS ]
then
    echo "Usage of $(basename $0):<filein><fileout><date1><date2>"
    exit 1
fi

filein=$1
fileout=$2
date1=$3
date2=$4

python extract_mentions_interval_one_interval_20160331.py -i <(zcat $filein) -d1 $date1 -d2 $date2 | gzip > $fileout
