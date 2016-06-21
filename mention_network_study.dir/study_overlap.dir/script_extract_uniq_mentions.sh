#!/bin/bash
NARGS=1

if [ $NARGS -ne $# ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<extracted_mention_dir>\e[0m\n"
    exit 1
fi

inputdir=$1
uniqdir=$inputdir/UNIQMENTIONS.dir

if [ ! -d $uniqdir ]
then
    mkdir -p $uniqdir
fi

for file in $inputdir/*.csv
do
    outfile=$uniqdir/$(basename $file | sed -re 's/\.csv//1')_UNIQUE_MENTIONS.csv
    cat $file | sort | uniq > $outfile
    echo -e "\e[3m$file\e[0m treated, result in \e[3m$outfile\e[0m"
done
