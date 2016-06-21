#!/bin/bash

NARGS=3

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<inputdir><listperiods><outputfile>\e[0m\n"
    exit 1
fi

dirin=$1
listp=$2
fout=$3

if [ -f $fout ]
then
    echo -e "\e[3m$fout\e[0m already exists, overwrite ? [Y/N]\t"
    read input
    if [ "$input" != "Y" ]
    then
        exit 1
    fi
fi

echo "Period,NbUsers,OverlapNeighbor,OverlapRandom" > $fout

while read line
do
    period=$(echo $line | cut -d , -f2)
    fileN=$(ls $dirin | grep "$period" | grep -i "neighbor")
    if [ -z $fileN ]
    then
        echo "No neighbor file found for period $period"
        continue
    fi

    fileR=$(ls $dirin | grep "$period" | grep -i "random")
    if [ -z $fileR ]
    then
        echo "No random file found for period $period"
        continue
    fi

    nU=$(wc -l $dirin/$fileN | awk '{print $1}')
    oN=$(cat $dirin/$fileN | sed '1d' | awk -F , 'BEGIN{sum=0;count=0}{sum+=$NF;count+=1}END{print sum/count}')
    oR=$(cat $dirin/$fileR | sed '1d' | awk -F , 'BEGIN{sum=0;count=0}{sum+=$NF;count+=1}END{print sum/count}')
    echo -e "${period},${nU},${oN},${oR}" >> $fout
    echo "Finish treating period $period"
done < <(cat $listp)
