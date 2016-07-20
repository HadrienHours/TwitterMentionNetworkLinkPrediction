#!/bin/bash

NARGS=5
debug=1
if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<fileInputs><listDates><dirOutputs><login><listmachines>\e[0m\n"
    exit 1
fi

fileInputs=$1
listDates=$2
dirOutputs=$3
userName=$4
listm=$5

if [ ! -d $dirOutputs ] && [ $debug -lt 2 ]
then
    mkdir -p $dirOutputs
fi

listmacs=$(echo $listm | sed -re 's/\.[a-z]+$//1')_${RANDOM}.tsv

if [ -f $listmacs ]
then
    rm $listmacs
fi

touch $listmacs

if [ $debug -lt 2 ]
then
    while read line
    do
        mac=$(echo $line | awk '{print $1}')
        res=$(ssh -n -o BatchMode=yes $userName@$mac "uname -n")
        if [ -z $res ]
        then
            echo "machine $mac seem not reachable, removed"
        else
            echo "$mac valid, added to list"
            echo $line >> $listmacs
        fi
    done < <(cat $listm)
else
    cp $listm $listmacs
fi


cwd=$(pwd)
CWD=$(echo $cwd | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")
DIROUT=$(echo $dirOutputs | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1") 

while read -u 3 date
do
    INPUT=$(echo $fileInputs | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")
    OUTPUT=$DIROUT/$(basename $fileInputs | sed -re 's/\.[a-z]+$//1')_USERS_TILL_TIME_${date}.tgz

    #Find available machine
    flag_f=0
    while [ $flag_f -eq 0 ]
    do
        while IFS='' read -r line || [[ -n "$line" ]]
        do
            mac=$(echo $line | awk '{print $1}')
            env=$(echo $line | awk '{print $2}')
            vl=$(ssh -o BatchMode=yes -n $userName@$mac "uname -n")
            if [ -z $vl ]
            then
                continue
            fi
            sc=$(ssh -n $userName@$mac "screen -ls" | grep -c -i "There is a screen on")
            if [ $sc -eq 0 ]
            then
                flag_f=1
                break
            fi
        done < <(cat $listmacs)
        if [ $flag_f -eq 0 ]
        then
            echo "All machines have been asigned a job, waiting 1 min before polling again"
            sleep 60
        fi
    done

    if [ $debug -gt 1 ]
    then
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m bash -c 'python extract_user_perperiod.py -i <(zcat $INPUT) -d $date | gzip > $OUTPUT')\""
    else
        if [ $debug -gt 0 ]
        then
            echo "At $(date) on $mac"
            echo "Extract user till date $date (output $OUTPUT)"
        fi   
        ssh $userName@$mac "(cd $CWD && screen -d -m bash -c 'python extract_user_perperiod.py -i <(zcat $INPUT) -d $date | gzip > $OUTPUT')"
    fi
done 3< <(cat $listDates)

rm $listmacs
