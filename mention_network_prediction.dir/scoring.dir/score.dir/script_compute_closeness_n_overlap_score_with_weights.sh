#!/bin/bash

NARGS=4
verbose=1
if [ $NARGS -ne $# ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<fileClosenessOverlap><weightCloseness><weightOverlap><fileOut>\e[0m\n"
    exit 1
fi

fileCAO=$1 #uid,mid,closeness,overlap
wC=$2
wO=$3
fileOut=$4
#filetemp=$(echo $fileOut | sed -re 's/\.csv//1')_tmp.csv

cat $fileCAO | grep -iv "id" | awk -v weightC=$wC -v weightO=$wO -F , 'BEGIN{OFS=","}{if($1>$2){print $2"-"$1,weightC*$3+weightO*$4}else{print $1"-"$2,weightC*$3+weightO*$4}}' | sort -t , -k1,1 >  $fileOut
if [ $verbose -gt 0 ]
then
    echo "Finished computing score for closeness and overalp"
fi

#cat $fileAO | grep -iv "id" | awk -F , 'BEGIN{OFS=","}{if($1>$2){print $2"-"$1,$4}else{print $1"-"$2,$4}}' >> $filetemp
#if [ $verbose -gt 0 ]
#then
#    echo "Finished adding overlap score"
#    echo "Start sorting"
#fi
#sort according to uid-mid
#cat $filetemp | sort -t , -k1,1 > $fileOut
#
#rm $filetemp
