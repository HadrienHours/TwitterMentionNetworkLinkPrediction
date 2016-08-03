#!/bin/bash
NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\t\e[1mUsage $(basename $0):<filein.tgz><fileout.csv>\e[0m"
    exit 1
fi
filein=$1
fileout=$2

echo "averagePercentagePrecision,averagePercentageRecall,averagePercentageF" > $fileout
zcat $filein | awk -F , 'BEGIN{avgP=0.0;avgR=0.0;avgF=0.0;counter=0;OFS=","}{avgP+=$1;avgR+=$2;avgF+=$3;counter+=1}END{print avgP/counter,avgR/counter,avgF/counter}' >> $fileout
