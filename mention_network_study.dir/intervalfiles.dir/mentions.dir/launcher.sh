#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo "Usage of $(basename $0):<filein><fileout>"
    exit 1
fi

filein=$1
fileout=$2
zcat $filein | sed -re 's/^[^{]+//1' | python extractmentions_20160322.py -o $fileout
