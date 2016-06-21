#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<dirfileswithsims><fileout>\n"
    tput sgr0
    echo -e "File with sims format:\n\e[3m\e[4mType,Count,Average,StandardDeviation\e[0m\n\e[3mMention,countM,avgM,stdM\nRandom,countR,avgR,stdM\e[0m"
    exit 1
fi

dirinputs=$1
fileout=$2

if [ -f $fileout ]
then
    echo -e "$fileout already exists. Overwrite ? [Y/N]:\t"
    read input
    if [ "$input" != "Y" ]
    then
        exit 1
    fi
fi

echo "Period,average_similarity_mention,average_similarity_random" > $fileout

for l in $dirinputs/*.csv
do 
    period=$(basename $l | egrep -o "[0-9]+\-[0-9]+")
    avgm=$(cat $l | awk -F , '{print $3}' | sed '1d'| head -1)
    avgr=$(cat $l | awk -F , '{print $3}' | sed '1d' | tail -1)
    echo "$period,$avgm,$avgr" >> $fileout
done
