#!/bin/bash

NARGS=5

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage of $(basename $0):<dircatvectors><dirusercouples><dirout><username><listmachines>\n"
    tput sgr0
    echo "Cat vectors:<uid,nCat1,...,nCatK"
    echo "User coules:<u1,u2>"
    echo "listmachine: <machinename  virtualenv>"
    exit 1
fi

debug=1

dircat=$1
dirm=$2
dirout=$3
user=$4
listm=$5
auxdir=$dirout/MENTIONSIMILARITY.dir

if [ ! -d $auxdir ]  && [ $debug -eq 0 ]
then
    mkdir -p $auxdir
fi

listmacs=$(echo $listm | sed -re 's/\.tsv//1')_${RANDOM}_tmp.csv

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

cwdt=`pwd`
cwd=$(echo $cwdt | sed -re "s/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1")
dirout2=$(echo $dirout | sed -re "s/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1")
auxdir2=$(echo $auxdir | sed -re "s/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1")

for file in $dirm/*.tgz
do
    #find corresponding cat vector file
    periodtst=$(basename $file | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")
    endPeriodTrn=$(echo $periodtst | cut -d _ -f1)
    if [ -z $endPeriodTrn ]
    then
        echo "No training period found for the testing period $periodtst"
        continue
    fi
    if [ $debug -gt 1 ]
    then
        echo -e "End training period found for testing period $periodtst:\t$endPeriodTrn"
    fi
    file2=$(basename $(ls $dircat/*.tgz | grep "_$endPeriodTrn\|\-$endPeriodTrn"))
    periodtrain=$(echo $file2 | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")

    if [ -z $file2 ]
    then
        echo "No cat vector found for period $periodtst ($periodtrain, $endPeriodTrn) in $dircat"
        continue
    else
        file2=$dircat/$file2
    fi

    if [ $debug -eq 1 ]
    then
        echo "For period $periodtst, file found for mention $file is"
        echo "$file2"
    fi

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
            sc=$(ssh -n $user@$mac "screen -ls" | grep -c -i "screen[s]* on")
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

    #rename output/input for remote machines
    OUTPUT1=$auxdir2/$(basename $file | sed -re 's/\.[a-z]+$//1')_MENTION_USER_SIMILARITY.tgz
    OUTPUT2=$auxdir2/$(basename $file | sed -re 's/\.[a-z]+$//1')_RANDOM_USER_SIMILARITY.tgz
    OUTPUT3=$dirout2/$(basename $file | sed -re 's/\.[a-z]+$//1')_AVERAGE_SIMILARITY_NEIGHBOR_VS_RANDOM.tgz
    INPUTM=$(echo $file | sed -re 's/\/media\/$user/\/datastore\/complexnet\/test_hours/1')
    INPUTC=$(echo $file2 | sed -re 's/\/media\/$user/\/datastore\/complexnet\/test_hours/1')
    if [ $debug -gt 1 ]
    then
        echo "ssh $user@$mac \"(cd $cwd && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; python computeaverageusersimilarity.py -c <(zcat $INPUTC) -u <(zcat $INPUTM) -o1 $OUTPUT1 -o2 $OUTPUT2 -o3 $OUTPUT3')\""
        echo -e "#######################################################################################################################################################################\n\n"
    else
        if [ $debug -gt 0 ]
        then
            echo -e "\n################################"
            echo "# On $mac ($env) at $(date)      #"
            echo -e "################################"
            echo "cmd launched python computeaverageusersimilarity.py -c <(zcat $INPUTC) -u <(zcat $INPUTM) -o1 $OUTPUT1 -o2 $OUTPUT2 -o3 $OUTPUT3"
        fi
        ssh $user@$mac "(cd $cwd && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; python computeaverageusersimilarity.py -c <(zcat $INPUTC) -u <(zcat $INPUTM) -o1 $OUTPUT1 -o2 $OUTPUT2 -o3 $OUTPUT3')"
    fi
done

rm $listmacs
