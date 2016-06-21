#!/bin/bash

NARGS=2

bold=$(tput bold)

if [ $# -ne $NARGS ]
then
    echo -e "\n\t${bold}Usage $(basename $0):<diroutuserhashes_labeled><dirout>\n"
    tput sgr0
    echo "User hash label format:<uid,hashcat>"
    exit 1
fi
dirhsh=$1
dirout=$2

if [ ! -d $dirout ]
then
    mkdir -p $dirout
fi

for filein in $dirhsh/*.csv
do
    fileout=$dirout/$(basename $filein | sed -re 's/\.csv//1')_CATVECTORS.csv
    echo "Userid,Category,Occurrences" > $fileout
    cat $filein | grep -iv "Userid" | sort -t , -n -k1,1 -k2,2 | uniq -c | awk 'BEGIN{OFS=","}{print $2,$1}' >> $fileout
    echo "$(basename $filein) treated"
done
