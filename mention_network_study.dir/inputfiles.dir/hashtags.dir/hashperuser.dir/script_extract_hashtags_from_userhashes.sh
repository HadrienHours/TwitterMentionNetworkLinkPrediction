#!/bin/bash

NARGS=3

if [ $# -ne $NARGS ]
then
	echo -e "\n\t\e[1mUsage $(basename $0):<diruserhashesperperiod><dirtweethashesperperiod><dirout>\e[0m\n"
	exit 1
fi

diruserhsh=$1
dirhshtweet=$2
dirout=$3

debug=2
if [ ! -d $dirout ]
then
	mkdir -p $dirout
fi

for l in $diruserhsh/*.csv
do
	period=$(basename $l | egrep -o "[0-9]{10}")
	filetwt=$(ls $dirhshtweet | grep "$period")
	if [ -z $filetwt ]
	then
		echo "No file could be found for period $period in $dirhshtweet"
		continue
    else
        if [ $debug -gt 1 ]
        then
            echo "File found for $period is $filetwt ($l)"
            read input
        fi
	fi
	fout=$dirout/HASHTWEETS_FILTEREDUSERSHASHTAGS_TILL_${period}.csv
    if [ $debug -gt 0 ]
    then
        echo "joining $filetwt with $l"
    fi
	#l: uid,hashtag
	#filetwt:hashtag,word1 word2...
	# join hashtag,word1 word2...,uid
    if [ $debug -gt 1 ]
    then
        echo "join -t , -11 -21 $dirhshtweet/$filetwt $l | awk -F , 'BEGIN{OFS=\",\"}{if(\$2){print \$1,\$2}}' > $fout"
    else
        join -t , -11 -22 $dirhshtweet/$filetwt $l | awk -F , 'BEGIN{OFS=","}{if($2){print $1,$2}}' > $fout
    fi
	echo -e "Treated period \e[1m$period\e[0m, result in \e[3m$fout\e[0m\n"
done
