#!/bin/bash

NARGS=4

debug=1

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<dirinputtraining_4weeks><dirout><login><listmachines>\e[0m\n"
    exit 1
fi


dirin=$1
dirout=$2
userName=$3
listm=$4

if [ ! -d $dirout ] && [ $debug -lt 2 ]
then
    mkdir -p $dirout
fi

#Test machines
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

DIRIN=$(echo $dirin | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")
DIROUT=$(echo $dirout | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")
CWD=$(echo $(pwd) | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")


for filein in $dirin/*.tgz
do
    FILEIN=$DIRIN/$(basename $filein)
    period=$(basename $filein | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")
    if [ -z $period ]
    then
        echo "No period found for $filein"
        continue
    fi
    FILEOUT=$DIROUT/OVERLAP_SCORE_FOR_EACH_POSSIBLE_LINK_TRAINING_MENTION_NETWORK_PERIOD_ENDING_${period}.tgz

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
            sc=$(ssh -n $userName@$mac "screen -ls" | grep -c -i "screen[s]* on")
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
        echo -e "Following command launched on \e[1m$mac\e[0m on \e[3m$(date)\e[0m"
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; python compute_overlap_score_from_mention_neighbor_dist.py -i1 <(zcat $FILEIN) -oo $FILEOUT')\""
        if [ $debug -gt 2 ]
        then
            echo "Type enter to continue"
            read input
        fi
    else 
        if [ $debug -gt 0 ]
        then
            echo -e "Following command launched on \e[1m$mac\e[0m on \e[3m$(date)\e[0m"
            echo "compute_overlap_score_from_mention_neighbor_dist.py -i1 $FILEIN -oo $FILEOUT"
        fi
        ssh $userName@$mac "(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; python compute_overlap_score_from_mention_neighbor_dist.py -i1 <(zcat $FILEIN) -oo $FILEOUT')"
    fi
done 

rm $listmacs
