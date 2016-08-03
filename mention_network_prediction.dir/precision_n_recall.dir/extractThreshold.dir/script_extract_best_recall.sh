#!/bin/bash
NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<dirInput><fileOut>\e[0m\n"
    exit 1
fi

dirInput=$1
fileout=$2

if [ -f $fileout ]
then
    echo "$fileout already exists. Overwrite ? [Y/N]"
    read input
    if [ "$input" != "Y" ]
    then
        exit 1
    fi
fi

echo "period,threshold,precision,recall" > $fileout

for l in $dirInput/*.csv
do
    period=$(basename $l | egrep -o "[0-9]{10}")
    bestl=$(cat $l | cut -d , -f1,6- | sort -rg -t , -k3,3 | head -1)
    echo "$period,$bestl" >> $fileout
done
