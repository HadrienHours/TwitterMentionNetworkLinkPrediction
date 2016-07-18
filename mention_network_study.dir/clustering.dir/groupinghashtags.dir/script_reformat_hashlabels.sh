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

for fin in $dirin/*.tgz
do
    echo -e "Treating file \e[3m$fin\e[0m"
    fout=$(echo $fin | sed -re 's/\.tgz//1')_REFORMATTED.tgz
    fstat=$sizdir/$(basename $fin | sed -re 's/\.tgz//1')_CLUSTERSIZES.tgz
    #remove index, non core points, convert float to int and sort hashes for future join
    zcat $fin | cut -d , -f2- | egrep -v ",$" | sed -re 's/\.0$//1' | sort -t  , -k1,1 | gzip > $fout
    zcat $fin | cut -d , -f2- | egrep -v ",$" | sed -re 's/\.0$//1' | cut -d , -f2 | sort -n | uniq -c | awk 'BEGIN{OFS=","}{print $2,$1}' | sort -n -t , -k1,1 | gzip > $fstat
    mv $fin $auxdir
    echo -e "\e[3m$fin\e[0m moved to \e[4m$auxdir\e[0m\n"
done
