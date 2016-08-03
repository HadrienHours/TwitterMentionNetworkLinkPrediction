#!/bin/bash

NARGS=7
debug=1
if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<dirInput><dirOutput><minthreshold><maxthreshold><step><listmachines><login>\e[0m\n"
    exit 1
fi

dirInput=$1
dirOutput=$2
minT=$3
maxT=$4
step=$5
listm=$6
userName=$7

if [ ! -d $dirOutput ]
then
    mkdir -p $dirOutput
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

CWD=$(echo $(pwd) | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIRINPUT=$(echo $dirInput | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIROUT=$(echo $dirOutput | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")

for l in $dirInput/*.tgz
do
    FILEOUT=$DIROUT/$(basename $l | sed -re 's/\.[a-z]+$//1')_PRECISON_AND_RECALL.tgz
    FILEIN=$DIRINPUT/$(basename $l)

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
            echo "All machines have been asigned max nb of jobs, waiting 1 min before polling again"
            sleep 60
        fi
    done

    if [ $debug -gt 1 ]
    then
        echo "ssh $userName@$mac \"(cd $CWD && screen -m -d bash -c 'python optimized_threshold_precision_overlap_min_max_threshold_compressed_files.py -i <(zcat $FILEIN) -m $minT -M $maxT -s $step | gzip -c > $FILEOUT')\""
    else
    if [ $debug -gt 0 ]
    then
        echo "On $mac at $(date)"
        echo "Computing precision and recall for $(basename $FILEIN), min $minT, max $maxT, step $step"
    fi
    ssh $userName@$mac "(cd $CWD && screen -m -d bash -c 'python optimized_threshold_precision_overlap_min_max_threshold_compressed_files.py -i <(zcat $FILEIN) -m $minT -M $maxT -s $step | gzip -c > $FILEOUT')"
    fi
done

rm $listmacs
