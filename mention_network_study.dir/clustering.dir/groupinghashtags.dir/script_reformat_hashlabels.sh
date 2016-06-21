#!/bin/bash

NARGS=1

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<dirhashlabel>$(tput sgr0)\n"
    exit 1
fi

dirin=$1
auxdir=$1/auxdir.dir
sizdir=$1/sizes.dir

if [ ! -d $auxdir ]
then
    mkdir $auxdir
fi

if [ ! -d $sizdir ]
then
    mkdir $sizdir
fi

for fin in $dirin/*.csv
do
    echo -e "Treating file \e[3m$fin\e[0m"
    fout=$(echo $fin | sed -re 's/\.csv//1')_REFORMATTED.csv
    fstat=$sizdir/$(basename $fin | sed -re 's/\.csv//1')_CLUSTERSIZES.csv
    #remove header and non core points, sort hashes for future join
    cat $fin | sed 1d | egrep -v ",$" | sort -t  , -k1,1 > $fout
    cat $fin | sed 1d | egrep -v ",$" | cut -d , -f2 | sort -n | uniq -c | awk 'BEGIN{OFS=","}{print $2,$1}' | sort -n -t , -k1,1 > $fstat
    mv $fin $auxdir
    echo -e "\e[3m$fin\e[0m moved to \e[4m$auxdir\e[0m\n"
done
