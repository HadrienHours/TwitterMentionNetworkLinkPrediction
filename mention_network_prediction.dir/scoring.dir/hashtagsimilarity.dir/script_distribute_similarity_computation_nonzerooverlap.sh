#!/bin/bash

NARGS=5

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage of $(basename $0):<dircatvectors><dirusercouples><dirout><login><listmachines>\n"
    tput sgr0
    echo "Cat vectors:<uid,nCat1,...,nCatK"
    echo "User couples:<u1,u2>"
    echo "listmachine: <machinename  virtualenv  numberSessions>"
    exit 1
fi

debug=1

dircat=$1
dirm=$2
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
DIRM=$(echo $dirm | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIRCAT=$(echo $dircat | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")

for file in $dirm/*.tgz
do
    #find corresponding cat vector file
    periodtrain=$(basename $file | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")
    period1=$(echo "$periodtrain" | egrep -o "^[0-9]{10}")
    period2=$(echo "$periodtrain" | egrep -o "[0-9]{10}$")
    if [ -z $periodtrain ]
    then
        echo "No training period found in $file"
        continue
    fi
    file2=$(basename $(ls $dircat/*.tgz | egrep "$period1[_-]{1}$period2"))

    if [ -z $file2 ]
    then
        echo "No cat vector found for period $periodtst ($periodtrain) in $dircat"
        continue
    fi

    #find a machine
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

    #rename output/input for remote machines
    FILECAT=$DIRCAT/$file2
    FILEM=$DIRM/$(basename $file)
    FILEOUT=$DIROUT/SIMILARITY_USER_COUPLE_NON_ZERO_OVERLAP_TRAINING_PERIOD_ENDING_${periodtrain}.tgz
    if [ $debug -gt 1 ]
    then
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; python computeaverageusersimilarity_fromOverlapCouples.py -c <(zcat $FILECAT) -m <(zcat $FILEM) | gzip > $FILEOUT')\""
        echo -e "#######################################################################################################################################################################\n\n"
    else
        if [ $debug -gt 0 ]
        then
            echo -e "\n################################"
            echo "# On $mac ($env) at $(date)      #"
            echo -e "################################"
            echo "cmd launched python computeaverageusersimilarity_fromOverlapCouples.py -c $FILECAT -m $FILEM -o $FILEOUT"
        fi
        ssh $userName@$mac "(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; python computeaverageusersimilarity_fromOverlapCouples.py -c <(zcat $FILECAT) -m <(zcat $FILEM) | gzip > $FILEOUT')"
    fi
done

rm $listmacs
