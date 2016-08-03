#!/bin/bash

NARGS=5

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage of $(basename $0):<dirOverlapHashSimPerTraininPeriod><dirTestingMentions><dirOut><login><listmachines>\n"
    tput sgr0
    echo "OverlapHashsim dir, tgzfiles, <uid,mid,overl,hashsim>"
    echo "listmachine: <machinename  virtualenv  numberSessions>"
    exit 1
fi

debug=1

dirTrain=$1
dirTest=$2
dirout=$3
userName=$4
listm=$5


if [ ! -d $dirout ]  && [ $debug -lt 2 ]
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
DIRTRAIN=$(echo $dirTrain | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")
DIRTEST=$(echo $dirTest | sed -re "s/\/media\/$userName\//\/datastore\/complexnet\/test_hours\//1")

for file in $dirTrain/*.tgz
do
    periodTrain=$(basename $file | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")
    period2=$(echo $periodTrain | egrep -o "[0-9]{10}$")

    fileTest=$(basename $(ls $dirTest/*.tgz | egrep "${period2}_[0-9]{10}"))
    if [ -z $fileTest ]
    then
        echo "No test file for training period $periodTrain ($period2) could be found in $dirTest)"
        echo "Period skipped"
        continue
    fi

    periodTest=$(echo $fileTest | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")

    FILETRAIN=$DIRTRAIN/$(basename $file)
    FILETEST=$DIRTEST/$fileTest
    FILEOUT=$DIROUT/$(basename $file | sed -re "s/TRAINING_PERIOD_${periodTrain}/TESTING_PERIOD_${periodTest}/1")


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
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m bash -c './assignscoreToTestingFile.sh $FILETEST $FILETRAIN $FILEOUT')\""
        echo -e "#######################################################################################################################################################################\n\n"
    else
        if [ $debug -gt 0 ]
        then
            echo -e "\n################################"
            echo "# On $mac ($env) at $(date)      #"
            echo -e "################################"
            echo -e "COMPUTING SCORE FOR \e[3m $FILETEST\e[0m WITH \e[3m $FILETRAIN\e[0m OUTPUT \e[1m$FILEOUT\e[0m"
        fi
        ssh $userName@$mac "(cd $CWD && screen -d -m bash -c './assignscoreToTestingFile.sh $FILETEST $FILETRAIN $FILEOUT')"
    fi
done

rm $listmacs
