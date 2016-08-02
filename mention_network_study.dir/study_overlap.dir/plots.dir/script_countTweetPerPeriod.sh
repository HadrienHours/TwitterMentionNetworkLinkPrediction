#!/bin/bash

NARGS=3
verbose=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\tUsage $(basename $0):<dirinputs><listPeriods><fileout>\n"
    exit 1
fi

dirinputs=$1
listPeriods=$2
fileout=$3


if [ -f $fileout ]
then
    echo -e "$fileout alread exists. Overwrite ? [Y/N]\t"
    read choice
    if [ "$choice" != "Y" ]
    then
        exit 1
    fi
fi

echo "Beginning,End,CountTweets" > $fileout

while read line
do
    date1=$(echo $line | cut -d , -f1 | cut -d \. -f1)
    date2=$(echo $line | cut -d , -f2 | cut -d \. -f1)
    flag=0
    counterG=0
    for file in $dirinputs/*.tgz
    do
        if [ $verbose -gt 1 ]
        then
            echo "Start parsing file $file for period [$date1 - $date2]"
        fi
        res=$(python countTweet_PerPeriod.py -i <(zcat $file) -d1 $date1 -d2 $date2)
        counter=$(echo $res | cut -d , -f2)
        counterG=$(( $counterG+$counter ))
        #suppose file.tgz are in chronological order
        #if found matching in previous files, not this one, no need to go further for this period
        if [ $counter -gt 0 ]
        then
            flag=1
        else
            if [ $flag -eq 1 ]
            then
                if [ $verbose -gt 0 ]
                then
                    echo "Stop crawling files for period [${date1}-${date2}], found 0 matching for file $(basename $file)"
                fi
                break
            fi
        fi
    done
    echo "$date1,$date2,$counterG" >> $fileout
done < <(cat $listPeriods)
