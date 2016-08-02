#!/bin/bash

NARGS=4
verbose=1
if [ $NARGS -ne $# ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<fileOverlapHashsim><weightOverlap><weightHashsim><fileOut>\e[0m\n"
    exit 1
fi

fileCAO=$1 #uid,mid,overlap,hashsim
wO=$2
wH=$3
fileOut=$4

v=$(echo "$wO $wH" | awk '{if($1+$2==1.0){print "yes"}}')
if [ "$v" != "yes" ]
then
    echo "Sum of the weights should be 1.0"
    exit 1
fi


zcat $fileCAO | grep -iv "id" | awk -v weightH=$wH -v weightO=$wO -F , 'BEGIN{OFS=","}{if($1>$2){print $2"-"$1,weightO*$3+weightH*$4}else{print $1"-"$2,weightO*$3+weightH*$4}}' | sort -t , -k1,1  | gzip -c >  $fileOut
if [ $verbose -gt 0 ]
then
    echo "Finished computing score for closeness and overalp for file $fileCAO"
fi
