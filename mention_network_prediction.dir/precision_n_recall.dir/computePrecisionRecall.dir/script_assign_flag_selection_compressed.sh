#!/bin/bash

NARGS=3

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<TrainFile.gz><TestFile.gz><OutputFile.gz>\e[0m\n"
    exit 1
fi

fileTrain=$1 #uid-mid,score
fileTest=$2
fileOut=$3

#detect separator "," or " "
pv=$(zcat $fileTrain | head -1 | awk -F , '{print NF}')
pe=$(zcat $fileTrain | head -1 | awk '{print NF}')

if [ $pv -eq 2 ]
then
    sep=1
elif [ $pe -eq 2 ]
then
    sep=2
else
    echo "Unrecognized input format"
    exit 1
fi


#
if [ $sep -eq 1 ]
then
    zcat $fileTrain $fileTest | sort | uniq -c | awk 'BEGIN{OFS=","}{if($1==1){print $2,0}else{print $2,1}}' | gzip > $fileOut
fi

if [ $sep -eq 2 ]
then
    zcat $fileTrain $fileTest | sort | uniq -c | awk 'BEGIN{OFS=","}{if($1==1){print $2,$3,0}else{print $2,$3,1}}' | gzip > $fileOut
fi
