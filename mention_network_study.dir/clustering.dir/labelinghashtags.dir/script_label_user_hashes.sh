#!/bin/bash

NARGS=3

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<dirhashlabels><diruserhashes><dirout>$(tput sgr0)\n"
    exit 1
fi

dirlabs=$1
diruserhsh=$2
dirout=$3

sortuserhsh=$dirout/auxdir.dir/sorteduserhashtags.dir
sortlabhsh=$dirout/auxdir.dir/sortedlabelhashtags.dir

if [ ! -d $sortuserhsh ]
then
    mkdir -p $sortuserhsh
fi

if [ ! -d $sortlabhsh ]
then
    mkdir -p $sortlabhsh
fi

for filelab in $dirlabs/*.csv
do
    period=$(basename $filelab | egrep -o "[0-9]{10}")
    fileuserhsh=$(ls $diruserhsh | grep "$period")
    if [ -z $fileuserhsh ]
    then
        echo -e "\e[31mNo file found in $diruserhsh for period $period\e[0m"
        echo -e "\e[31mSkipped\e[0m"
        continue
    fi

    echo -e "For period \e[1m$period\e[0m find matching file: \e[3m$fileuserhsh\e[0m"

    f1=$sortuserhsh/$(basename $fileuserhsh | sed -re 's/\.csv//1')_SORTED.csv
    f2=$sortlabhsh/$(basename $filelab | sed -re 's/\.csv//1')_SORTED.csv
    cat $filelab | sort -t , -k1,1 > $f2
    cat $diruserhsh/$fileuserhsh | sort -t , -k2,2 > $f1
    fout=$dirout/$(basename $fileuserhsh | sed -re 's/\.csv//1')_LABELED_DBSCAN.csv
    join -t , -12 -21 $f1 $f2 | cut -d , -f2- > $fout
    echo -e "File treated, result stored in \e[3m$fout\e[0m\n"
done
