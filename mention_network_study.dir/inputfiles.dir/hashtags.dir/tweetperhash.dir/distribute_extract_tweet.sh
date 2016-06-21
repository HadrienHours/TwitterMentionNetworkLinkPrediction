#!/bin/bash

NARGS=4

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<dirinput><diroutput><username><listmachines>$(tput sgr0)\n"
    echo "Input dir contains tgz files"
    echo "Output dir will contain csv file with extracted hash tweets"
    echo "List machine: tsv file <machine><environment>"
    exit 1
fi

dirin=$1
dirout=$2
user=$3
listm=$4

listmacs=${listm}_tmp
debug=0

if [ -f $listmacs ]
then
    rm $listmacs
fi

touch $listmacs

if [ $debug -eq 0 ]
then
    while read line
    do
        mac=$(echo $line | awk '{print $1}')
        res=$(ssh -n -o BatchMode=yes $user@$mac "uname -n")
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

if [ $debug -eq 0 ]
then
    if [ -d $dirout ]
    then
        echo -e "$dirout already exists. Continue (risk of overwritting) [Y/N]:\t"
        read input
        if [ "$input" == "Y" ]
        then
            echo "ok"
        else
            exit 1
        fi
    else
        mkdir -p $dirout
    fi
fi

for file in $dirin/*.tgz
do
    #find a machine with no job running
    flag_f=0
    while [ $flag_f -eq 0 ]
    do
        while IFS='' read -r line || [[ -n "$line" ]]
        do
            mac=$(echo $line | awk '{print $1}')
            env=$(echo $line | awk '{print $2}')
            vl=$(ssh -o BatchMode=yes -n $user@$mac "uname -n")
            if [ -z $vl ]
            then
                continue
            fi
            sc=$(ssh -n $user@$mac "screen -ls" | grep -c -i "There is a screen on")
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

    fileout=$dirout/$(basename $file | sed -re 's/\.tgz//1')_tweetperhash.csv
    ./script_extract_hashtweet_distributed.sh $file $fileout $mac $env
done

rm $listmacs
