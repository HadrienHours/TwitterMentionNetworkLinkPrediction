#!/bin/bash

NARGS=6

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage of $(basename $0):<dirOverlapHashSimPerTraininPeriod><weightOverlap><weightHashsim>i<dirOut><login><listmachines>\n"
    tput sgr0
    echo "Overlap dir, tgzfiles, <uid,mid,overl>"
    echo "Hashsim dir, tgzfiles, <uid,mid,overl>"
    echo "listmachine: <machinename  virtualenv  numberSessions>"
    exit 1
fi

debug=2

dirInput=$1
weightO=$2
weightH=$3
dirout=$4
userName=$5
listm=$6

v=$(echo "$weightO $weightH" | awk '{if($1+$2==1.0){print "yes"}}')
if [ "$v" != "yes" ]
then
    echo "Sum of the weights should be 1.0"
    exit 1
fi


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
DIRIN=$(echo $dirInput| sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
wO=$(echo $weightO | tr \. \-)
wH=$(echo $weightH | tr \. \-)

for file in $dirInput/*.tgz
do
    periodTrain=$(basename $file | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")
    FILEOUT=$DIROUT/SCORE_WEIGHT_OVERLAP_${wO}_WEIGHT_HASHSIM_${wH}_TRAINING_PERIOD_${periodTrain}.tgz
    FILEIN=$DIRIN/$(basename $file)

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
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m ./script_compute_closeness_n_overlap_score_with_weights.sh $FILEIN $weightO $weightH $FILEOUT)\""
        echo -e "#######################################################################################################################################################################\n\n"
    else
        if [ $debug -gt 0 ]
        then
            echo -e "\n################################"
            echo "# On $mac ($env) at $(date)      #"
            echo -e "################################"
            echo "COMPUTING SCORE FOR $(basename $FILEIN) OUTPUT $(basename $FILEOUT)"
        fi
        ssh $userName@$mac "(cd $CWD && screen -d -m ./script_compute_closeness_n_overlap_score_with_weights.sh $FILEIN $weightO $weightH $FILEOUT)"
    fi
done

rm $listmacs
