#!/bin/bash

NARGS=2

if [ $NARGS -ne $# ]
then
	echo -e "\n\t\e[1mUsage $(basename $0):<inputMentionsDir><outputListUsersDir>\e[0m\n"
	exit 1
fi

dirin=$1
dirout=$2

if [ ! -d $dirout ]
then
	mkdir $dirout
fi

for l in $dirin/*.csv
do
	period=$(basename $l | egrep -o "[0-9]+")
	fout=$dirout/LISTUSERSINMENTIONS_UNTIL_${period}_SORTED_UID.csv
	cat $l | grep -iv "id" | tr , "\n" | sort | uniq > $fout
	echo -e "\e[3m$l\e[0m treated, result in \e[3m$fout\e[0m"
done
