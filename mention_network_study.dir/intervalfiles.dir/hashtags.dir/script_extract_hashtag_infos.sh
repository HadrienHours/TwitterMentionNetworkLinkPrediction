#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<filein.tgz><fileout.tgz>\e[0m\n"
    exit 1
fi

filein=$1
fileout=$2

python extractHashtagInformation.py -i <(zcat $filein) | gzip > $fileout
