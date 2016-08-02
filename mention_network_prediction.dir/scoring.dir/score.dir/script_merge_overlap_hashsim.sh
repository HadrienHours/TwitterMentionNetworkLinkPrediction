#!/bin/bash
NARGS=3

if [ $# -ne $NARGS ]
then
    echo -e "\t\e[1mUsage $(basename $0):<fileoverlap><filehashsim><fileout>\e[0m\n"
    exit 1
fi

fileO=$1
fileH=$2
fileout=$3

dirTmp=$(dirname $fileout)

fileOS=$dirTmp/$(basename $fileO | sed -re 's/\.[a-z]+$//1')_SORTED.tgz
fileHS=$dirTmp/$(basename $fileH | sed -re 's/\.[a-z]+$//1')_SORTED.tgz

zcat $fileO | awk -F , 'BEGIN{OFS=","}{if($1>$2){print $2"-"$1,$3}else{print $1"-"$2,$3}}' | sort | uniq | sort -t , -k1,1 | gzip -c > $fileOS
zcat $fileH | awk -F , 'BEGIN{OFS=","}{if($1>$2){print $2"-"$1,$3}else{print $1"-"$2,$3}}' | sort | uniq | sort -t , -k1,1 | gzip -c > $fileHS

join -t , -11 <(zcat $fileOS) -21 <(zcat $fileHS) | sed -re 's/([0-9]+)\-([0-9]+)/\1\,\2/1' | sed '1iUser1ID,User2ID,Overlap,HashSime' | gzip -c > $fileout

rm $fileOS $fileHS
