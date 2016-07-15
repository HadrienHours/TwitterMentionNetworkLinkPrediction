#!/bin/bash

NARGS=4
debug=1
renice=0

if [ $NARGS -ne $# ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<inputdir><outputdir><login><listmachines>$(tput sgr0)\n"
    exit 1
fi

dirin=$1
dirout=$2
userName=$3
listm=$4

if [ ! -d $dirout ]
then
    mkdir -p $dirout
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
DIROUT=$(echo $dirout | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")

for filein in $dirin/*.tgz
do
    #find machine with no job running
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

    FILEIN=$(echo $filein | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
    FILEOUT=$DIROUT/$(basename $filein | sed -re 's/\.[a-z]+$//1')_HASH_PER_USER.tgz
    if [ $debug -gt 1 ]
    then
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m ./script_extract_userhashes_from_intervalfiles.sh $FILEIN $FILEOUT)\""
    else
        if [ $debug -gt 0 ]
        then
            echo -e "\n################################"
            echo "# On $mac ($env) at $(date)      #"
            echo -e "################################"
            echo "Extracting user hashtag for file $(basename $FILEIN)"
        fi
        ssh -n $userName@$mac "(cd $CWD && screen -d -m ./script_extract_userhashes_from_intervalfiles.sh $FILEIN $FILEOUT)"
        if [  $renice -gt 0 ]
        then
            ssh -n $userName@$mac "renice -n 5 -u $userName"
        fi
    fi

done
