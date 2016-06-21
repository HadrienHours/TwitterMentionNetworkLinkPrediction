#!/bin/bash

NARGS=3

if [ $NARGS -ne $# ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<directory_user_in_mentions><conversion table><outputdir>\n"
    tput sgr0
    exit 1
fi

dirum=$1
convt=$2
dirout=$3

if [ ! -d $dirout ]
then
    mkdir -p $dirout
fi

while read line
do
    p1=$(echo $line | awk -F , '{print $1}')
    p2=$(echo $line | awk -F , '{print $2}')
    filein=$(ls $dirum/*.csv | grep "$p1")
    if [ -z $filein ]
    then
        echo "No file found for $p1 in $dirum"
        continue
    fi
    fileout=$dirout/$(basename $filein | sed -re 's/\.csv//1')_CLOSENESSPERIOD_${p2}.csv
    cp $filein $fileout
    echo "$(basename $filein) converted to $(basename $fileout)"
done < <(cat $convt)
