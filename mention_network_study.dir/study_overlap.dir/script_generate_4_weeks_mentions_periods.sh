#!/bin/bash

NARGS=3
debug=1

if [ $# -ne $NARGS ]
then
    echo "Usage $(basename $0):<dirin><dirout><listperiods>"
    exit 1
fi


dirin=$1
dirout=$2
listperiods=$3
while read line
do 
    period1=$(echo $line | cut -d , -f1)
    period2=$(echo $line | cut -d , -f2)
    file1=$(ls $dirin | grep "$period1")
    file2=$(ls $dirin | grep "$period2")
    if [ -z $file1 ]
    then
        echo "No file was found for period $period1 in $dirin"
        continue
    else
        if [ $debug -gt 0 ]
        then
            echo "File $file1 found for $period1 in $dirin"
        fi
    fi
    if [ -z $file2 ]
    then
        echo "No file was found for period $period2 in $dirin"
        continue
    else
        if [ $debug -gt 0 ]
        then
            echo "File $file2 found for period $period2 in $dirin"
        fi
    fi
    fileout="$dirout/mentions_per_period_${period1}-${period2}_cumulative.csv"
    cat $dirin/$file1 $dirin/$file2 > $fileout
    echo -e "Generate file \e[1m$fileout\e[0m with \e[3m$file1\e[0m and \e[3m$file2\e[0m"
done < <(cat $listperiods)
