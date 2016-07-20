#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\nUsage $(basename $0):<filein.tgz><fileout.tgz>\n"
    exit 1
fi

filein=$1
fileout=$2

python extract_user_first_activity.py -i <(zcat $filein | sort -g -t , -k1,1 -k2,2) | gzip > $fileout
