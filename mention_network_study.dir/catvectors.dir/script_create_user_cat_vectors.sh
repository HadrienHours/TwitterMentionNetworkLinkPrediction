#!/bin/bash

NARGS=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<dircatstreams><dirout>\n"
    tput sgr0
    exit 1
fi

dircatstream=$1
dirout=$2
nCats=$3

if [ ! -d $dirout ]
then
    mkdir -p $dirout
fi

for filestream in $dircatstream/*.tgz
do
    fileout=$dirout/$(basename $filestream | sed -re 's/\.tgz//1')_FULLVECTORS.tgz
    echo "Start vectorizing $(basename $filestream)"
    nc=$(zcat $filestream | cut -d , -f2 | sort -n | uniq | sort -rn | head -1)
    nCats=$(( $nc+1 ))
    python create_vectors.py -i <(zcat $filestream) -c $nCats | gzip > $fileout
done
