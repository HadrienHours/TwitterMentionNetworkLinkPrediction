#!/bin/bash

NARGS=4
debug=2
if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<listInputs><dirOutputs><login><listmachines>\e[0m\n"
    exit 1
fi

listInputs=$1
dirOutputs=$2
userName=$3
listm=$4

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

while read -u 3 line
do
    INPUT=$(echo $line | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")
    OUTPUT=$DIROUT/$(basename $line | sed -re 's/\.[a-z]+$//1')_EXTRACTED_USER_ACTIVITY.tgz

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
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate;python extract_user_activity.py -i <(zcat $INPUT) | gzip > $OUTPUT')\""
    else
        if [ $debug -gt 0 ]
        then
            echo "At $(date) on $mac"
            echo "Extract user activity from file $INPUT (output $OUTPUT)"
        fi   
        ssh $userName@$mac "(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate;python extract_user_activity.py -i <(zcat $INPUT) | gzip > $OUTPUT')"
    fi
done 3< <(cat $listInputs)

rm $listmacs
