#!/bin/bash

NARGS=3

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<dirin><dirout><listperiods>$(tput sgr0)\n"
    exit 1
fi

dirin=$1
dirout=$2
listperiods=$3

while read line
do
    period=$(echo $line | egrep -o "[0-9]+\_[0-9]+")

    echo -e "Start treating period \e[1m$period\e[0m"
    filein=$(ls $dirin | grep "$period")
    filein=$dirin/$(basename $filein)
    if [ -z $filein ]
    then
        echo "No file found for period $period, program will exit now"
        exit 1
    else
        echo -e "For period $period:\t$filein"
    fi

    fout=$dirout/$(basename $filein | sed -re 's/\.csv//1')_cumulative.csv

    if [ -z $prev ]
    then
        cat $filein > $fout
    else
        cat $prev $filein > $fout
    fi
    prev=$fout
done < <(cat $listperiods)
