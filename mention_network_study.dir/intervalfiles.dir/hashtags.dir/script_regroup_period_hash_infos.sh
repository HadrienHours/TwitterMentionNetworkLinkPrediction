#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<listDates><dirInputs>\e[0m"
    exit 1
fi

listDates=$1
dirin=$2
dirout=$3

flagrm=0

while read lineDate
do
    date1=$(echo $lineDate | cut -d , -f1 | cut -d \. -f1)
    date2=$(echo $lineDate | cut -d , -f2 | cut -d \. -f1)
    fileout=$dirin/HASH_INFO_PERIOD_${date1}-${date2}_SORTED_CHRONOLOGICALLY.tgz
    for l in $dirin/*${date1}-${date2}.tgz
    do
        zcat $l
    done | sort -g -t , -k1,1 | gzip > $fileout
    if [ $flagrm -gt 0 ]
    then
        rm $dirin/*${date1}-${date2}.tgz
    fi
    echo "Finish treating period $date1 - $date2"
done < <(cat $listDates)
