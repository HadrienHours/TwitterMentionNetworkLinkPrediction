#/bin/bash
NARGS=3

if [ $# -ne $NARGS ]
then
    echo -e "\t\e[1mUsage $(basename $0):<fileTest><fileTrainWithScore><fileOut>\e[0m"
    exit 1
fi

flagRM=1

fileTest=$1
fileTrain=$2
fileOut=$3

dirTmp=$(dirname $fileOut)
fileTestS=$dirTmp/$(basename $fileTest | sed -re 's/\.[a-z]+$//1')_SORTED.tgz

zcat $fileTest | awk -F , '{if($1>$2){print $2"-"$1}else{print $1"-"$2}}' | sort | gzip -c > $fileTestS
join -t , -11 <(zcat $fileTestS) -21 <(zcat $fileTrain) | gzip -c > $fileOut

if [ $flagRM -gt 0 ]
then
    rm $fileTestS
fi
