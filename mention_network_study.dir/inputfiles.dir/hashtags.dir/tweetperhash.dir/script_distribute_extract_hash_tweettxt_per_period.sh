#!/bin/bash

NARGS=4
debug=1

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<dirInputs><dirOutputs><listmachines><login>\e[0m\n"
    exit 1
fi

dirIn=$1
dirOut=$2
listm=$3
userName=$4

if [ ! -d $dirOut ]
then
    mkdir -p $dirOut
fi

listmacs=$(basename $listm | sed -re 's/\.[a-z]+$//')_${RANDOM}.tsv

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

cwd=`pwd`
CWD=$(echo $cwd | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIROUT=$(echo $dirOut | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")

for l in $dirIn/*.tgz
do
    #find a machine with no job running
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

    FILEIN=$(echo $l | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
    FILEOUT=$DIROUT/$(basename $l | sed -re 's/\.[a-z]+//1')_HASH_TWEETS_ORDERED_HASH.tgz

    if [ $debug -gt 1 ]
    then
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m ./script_extract_hash_tweettxt_per_period.sh $FILEIN $FILEOUT\""
    else
        if [ $debug -gt 0 ]
        then
            echo -e "\n################################"
            echo "# On $mac ($env) at $(date)      #"
            echo -e "################################"
            echo "Extracting hashinfo for period $date1 - $date2 from file $(basename $l)"
        fi
        ssh -n $userName@$mac "(cd $CWD && screen -d -m bash ./script_extract_hash_tweettxt_per_period.sh $FILEIN $FILEOUT)"
    fi
done

rm $listmacs




