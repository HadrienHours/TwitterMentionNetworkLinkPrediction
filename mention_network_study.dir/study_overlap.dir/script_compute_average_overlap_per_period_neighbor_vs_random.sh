#!/bin/bash
NARGS=3

verbose=1

if [ $NARGS -ne $# ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<dirinput><listperiods><fileout>\e[0m\n"
    exit 1
fi

dirin=$1
listperiods=$2
fileout=$3

if [ -f $fileout ]
then
    echo -e "$fileout seems to already exist, overwrite ? [Y/N]:\t"
    read input
    if [ "$input" != "Y" ]
    then
        exit 1
    fi
fi

echo "Period,NumberMentions,AverageOverlapNeighbor,AverageOverlapRandom" > $fileout

nlines=$(wc -l $listperiods | awk '{print $1}')
counter=0
while read line
do
    counter=$(( $counter+1 ))
    if [ $(( $counter%10 )) -eq 0 ]
    then
        echo "$counter/$nlines done"
    fi
    period=$(echo $line | cut -d , -f2)
    fileNeighbor=$(ls $dirin | grep "$period" | grep -i "neighbor")
    fileRandom=$(ls $dirin | grep "$period" | grep -i "random")

    if [ -z $fileNeighbor ] || [ -z $fileRandom ]
    then
        if [ $verbose -gt 0 ]
        then
            echo "No file could be found for neighbor or random in $dirin for period $period, skipped"
        fi
        continue
    fi

    avgN=$(cat $dirin/$fileNeighbor | egrep -iv "id" | egrep -v ",-1$|,-2$" | awk -F , 'BEGIN{count=0;sum=0}{count+=1;sum+=$NF}END{print sum/count}')
    avgR=$(cat $dirin/$fileRandom | egrep -iv "id" | awk -F , 'BEGIN{count=0;sum=0}{count+=1;sum+=$NF}END{print sum/count}')
    nbUsers=$(wc -l $dirin/$fileRandom | awk '{print $1}')
    echo "$period,$nbUsers,$avgN,$avgR" >> $fileout
done < <(cat $listperiods)
