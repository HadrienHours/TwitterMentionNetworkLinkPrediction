#!/bin/bash

NARGS=5
debug=1
if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<dirTraining><dirTesting><dirOut><listMachines><login>\e[0m\n"
    exit 1
fi

dirTrain=$1
dirTest=$2
dirOut=$3
listm=$4
userName=$5

if [ ! -d $dirOut ]
then
    mkdir -p $dirOut
fi

listmacs=$(echo $listm | sed -re 's/\.tsv//1')_${RANDOM}_tmp.csv

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
DIRTRAIN=$(echo $dirTrain | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIRTEST=$(echo $dirTest | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIROUT=$(echo $dirOut | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")

for fileTest in $dirTest/*.tgz
do
    periodTest=$(basename $fileTest | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")
    period1=$(echo $periodTest | egrep -o "^[0-9]{10}")
    fileTrain=$(ls $dirTrain/*.tgz | egrep "[0-9]{10}[_\-]{1}$period1")

    if [ -z $fileTrain ]
    then
        echo "No train file found for test period $periodTest ($period1) in $dirTrain"
        echo "Skipped"
        continue
    fi

    FILETRAIN=$DIRTRAIN/$(basename $fileTrain)
    FILETEST=$DIRTEST/$(basename $fileTest)
    FILEOUT=$DIROUT/$(basename $fileTrain | sed -re 's/\.csv//1')_ASSIGNED_FLAG.gz

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
        echo "ssh $userName@$mac \"(cd $CWD && screen -m -d bash -c './script_assign_flag_selection_compressed.sh $FILETRAIN $FILETEST $FILEOUT')\""
    else
        if [ $debug -gt 0 ]
        then
            echo "On $mac at $(date)"
            echo "Assigning flag selection to $FILETRAIN with $FILETEST, output $FILEOUT"
        fi
        ssh $userName@$mac "(cd $CWD && screen -m -d bash -c './script_assign_flag_selection_compressed.sh $FILETRAIN $FILETEST $FILEOUT')"
    fi
done

rm $listmacs

