#!/bin/bash

NARGS=5

if [ $NARGS -ne $# ]
then
    echo -e "$(tput bold)Usage $(basename $0):<dirinputs><diroutputhashes><diroutputuserhashes><diroutputhasheshashes><date>$(tput sgr0)"
    exit 1
fi

dirinput=$1
dirouthsh=$2
diroutusrhsh=$3
dirouthshhsh=$4
dt=$5


#Assume diroutput created, should be checked by master script Avoid overwrite
YEAR=$(date +%Y -d @$dt)
MONTH=$(date +%m -d @$dt)

#echo -e "For $dt\nYear:\t$YEAR\nMonth:\t$MONTH"

fileouthsh=$dirouthsh/hashes_per_period_period_${dt}.csv
fileoutusrhsh=$diroutusrhsh/user_hashes_per_period_period_${dt}.csv
fileouthshhsh=$dirouthshhsh/hash_hashes_per_period_period_${dt}.csv

source /datastore/complexnet/test_hours/hadrien3/bin/activate

for l in $dirinput/*.tgz
do
    #check valid entry
    year=$(basename $l | cut -d \. -f1 | cut -d \- -f1)
    month=$(basename $l | cut -d \. -f1 | cut -d \- -f2)
    if [ $year -gt $YEAR ]
    then
        echo "$l discarded for date $dt"
        continue
    fi
    if [ $month -gt $MONTH ]
    then
        echo "$l discarded for date (month) $dt"
        continue
    fi

    zcat $l | python extract_hash_per_period.py -o1 $fileouthsh -o2 $fileoutusrhsh -o3 $fileouthshhsh -d $dt
    echo "File $l treated by machine $(hostname) for date $dt (${YEAR}-${MONTH})"
done
