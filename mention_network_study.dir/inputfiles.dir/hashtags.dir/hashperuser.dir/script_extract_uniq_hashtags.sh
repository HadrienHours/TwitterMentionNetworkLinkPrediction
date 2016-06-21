#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo "Usage $(basename $0):<dirUserHashe><dirout>"
    exit 1
fi

dirin=$1
dirout=$2

for l in $dirin/*.csv
do
    fout=$dirout/$(basename $l | sed -re 's/\.csv//1')_UNIQ.csv
    cat $l | cut -d , -f2 | egrep -v "^[ \t]*$" | sort | uniq > $fout
    echo "$l treated"
done
