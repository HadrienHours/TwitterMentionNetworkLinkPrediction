#!/bin/bash

NARGS=5

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage of $(basename $0):<dirOverlapPerTraininPeriod><dirHashSimPerTraininPeriod><dirout><login><listmachines>\n"
    tput sgr0
    echo "Overlap dir, tgzfiles, <uid,mid,overl>"
    echo "Hashsim dir, tgzfiles, <uid,mid,overl>"
    echo "listmachine: <machinename  virtualenv  numberSessions>"
    exit 1
fi

debug=1

dirOverlap=$1
dirHashsim=$2
dirout=$3
userName=$4
listm=$5

if [ ! -d $dirout ]  && [ $debug -eq 0 ]
then
    mkdir -p $dirout
fi

listmacs=$(echo $listm | sed -re 's/\.tsv//1')_${RANDOM}_tmp.tsv

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


cwdt=`pwd`
CWD=$(echo $cwdt | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIROUT=$(echo $dirout | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIRO=$(echo $dirOverlap | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIRH=$(echo $dirHashsim | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")


for fileO in $dirOverlap/*.tgz
do
    periodTrain=$(basename $fileO | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")
    period1=$(echo $periodTrain | egrep -o "^[0-9]{10}")
    period2=$(echo $periodTrain | egrep -o "[0-9]{10}$")
    fileH=$(basename $(ls $dirHashsim/*.tgz | egrep "$period1[_\-]{1}$period2"))
    
    if [ -z $fileH ]
    then
        echo -e "\tNo file found for period [$period1,$period2] in $dirHashim"
        echo -e "Period \e[1m$periodTrain\e[0m skipped"
        continue
    fi

    FILEO=$DIRO/$(basename $fileO)
    FILEH=$DIRH/$fileH
    FILEOUT=$DIROUT/USER_OVERLAP_HASHSIM_TRAINING_PERIOD_${periodTrain}.tgz

    #Find available machine
    flag_f=0
    while [ $flag_f -eq 0 ]
    do
        while IFS='' read -r line || [[ -n "$line" ]]
        do
            mac=$(echo $line | awk '{print $1}')
            env=$(echo $line | awk '{print $2}')
            nS=$(echo $line | awk '{print $3}')
            vl=$(ssh -o BatchMode=yes -n $userName@$mac "uname -n")
            if [ -z $vl ]
            then
                continue
            fi
            nsc=$(ssh -n $userName@$mac "screen -ls | egrep -i \"socket[s]* in /var\"" | awk '{print $1}')
            if [ -z $nsc ] || [ $nsc -lt $nS ]
            then
                flag_f=1
                break
            fi
        done < <(cat $listmacs)
        if [ $flag_f -eq 0 ]
        then
            echo "All machines have been asigned their maximum number of jobs, waiting 1 min before polling again"
            sleep 60
        fi
    done

    if [ $debug -gt 1 ]
    then
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m ./script_merge_overlap_hashsim.sh $FILEO $FILEH $FILEOUT)\""
        echo -e "#######################################################################################################################################################################\n\n"
    else
        if [ $debug -gt 0 ]
        then
            echo -e "\n################################"
            echo "# On $mac ($env) at $(date)      #"
            echo -e "################################"
            echo "MERGING FILES $(basename $FILEO) and $(basename $FILEH) into $(basename $FILEOUT)"
        fi
        ssh $userName@$mac "(cd $CWD && screen -d -m ./script_merge_overlap_hashsim.sh $FILEO $FILEH $FILEOUT)"
    fi
done

rm $listmacs
