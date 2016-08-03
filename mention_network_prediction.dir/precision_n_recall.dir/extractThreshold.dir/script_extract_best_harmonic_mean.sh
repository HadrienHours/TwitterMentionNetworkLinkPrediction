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

echo "period,threshold,precision,recall,harmonicmean" > $fileout

for l in $dirInput/*.tgz
do
    period=$(basename $l | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")
    #File threshold,TP,FP,TN,FN,Precision,Recall
    bestl=$(zcat $l |  cut -d , -f1,6- | awk -F , 'BEGIN{OFS=","}{if(($2+$3) != 0){print $1,$2,$3,2*($3*$2)/($3+$2)}}' | sort -rg -t , -k4,4 | head -1)
    echo "$period,$bestl" >> $fileout
done

ft=${fileout}.gz
fo=$(echo $fileout | sed -re 's/\.[a-z]+$//1').tgz
gzip $fileout
mv $ft $fo
