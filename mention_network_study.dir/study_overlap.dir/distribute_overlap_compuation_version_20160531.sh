#!/bin/bash

NARGS=6

debug=1

if [ $# -ne $NARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<dirinputtraining_4weeks><dirinputtesting_2weeks><dir_users><dirout><listperiods><listmachines>\e[0m\n"
    echo "List period:<period in filename training,period in filename testing>"
    echo -e "List mechine (tsv):<name_machine\tenvrionment>"
    exit 1
fi


dirintrn=$1
dirintst=$2
dirusers=$3
dirout=$4
listperiods=$5
listm=$6

auxdir=$dirout/aux.dir

if [ ! -d $auxdir ]
then
    mkdir -p $auxdir
fi

#Test machines
listmacs=$(echo $listm | sed -re 's/\.tsv//1')_${RANDOM}.csv

if [ -f $listmacs ]
then
    rm $listmacs
fi

touch $listmacs

if [ $debug -lt 3 ]
then
    while read line
    do
        mac=$(echo $line | awk '{print $1}')
        res=$(ssh -n -o BatchMode=yes hhours@$mac "uname -n")
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

DIRINTST=$(echo $dirintst | sed -re 's/\/media\/hhours/\/datastore\/complexnet\/test_hours/1')
DIRINTRN=$(echo $dirintrn | sed -re 's/\/media\/hhours/\/datastore\/complexnet\/test_hours/1')
DIRUSERS=$(echo $dirusers | sed -re 's/\/media\/hhours/\/datastore\/complexnet\/test_hours/1')
DIROUT=$(echo $dirout | sed -re 's/\/media\/hhours/\/datastore\/complexnet\/test_hours/1')
AUXDIR=$DIROUT/aux.dir
CWD=$(echo $(pwd) | sed -re 's/\/media\/hhours/\/datastore\/complexnet\/test_hours/1')

while read -u 3 line
do
    periodtrn=$(echo $line | cut -d , -f1)
    periodtst=$(echo $line | cut -d , -f2)
    filetrn=$(ls $dirintrn | grep "$periodtrn")
    filetst=$(ls $dirintst | grep "$periodtst")
    fileusr=$(ls $dirusers | grep "$periodtrn")

    if [ -z $filetrn ] || [ -z $filetst ] || [ -z $fileusr ]
    then
        echo "Could not find files in $dirintrn, $dirusers and $dirintst for period $periodtrn and $periodtst respectively, skipped"
        continue
    fi

    FILETRN=$DIRINTRN/$(basename $filetrn)
    FILETST=$DIRINTST/$(basename $filetst)
    FILEUSR=$DIRUSERS/$(basename $fileusr)
    FILEOUTNB=$DIROUT/OVERLAP_MENTION_NETWORK_PERIODS_${periodtrn}_FOR_MENTION_IN_PERIOD_${periodtst}_NEIGHBORS.csv
    FILEOUTRN=$DIROUT/OVERLAP_MENTION_NETWORK_PERIODS_${periodtrn}_FOR_MENTION_IN_PERIOD_${periodtst}_RANDOMS.csv
    VECTFILE=$AUXDIR/ADJACENCY_VECTORS_MENTION_NETWORKS_PERIOD_ENDING_${periodtrn}.csv

    #Find available machine
    flag_f=0
    while [ $flag_f -eq 0 ]
    do
        while IFS='' read -r line || [[ -n "$line" ]]
        do
            mac=$(echo $line | awk '{print $1}')
            env=$(echo $line | awk '{print $2}')
            vl=$(ssh -o BatchMode=yes -n hhours@$mac "uname -n")
            if [ -z $vl ]
            then
                continue
            fi
            sc=$(ssh -n hhours@$mac "screen -ls" | grep -c -i "There is a screen on")
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

    if [ $debug -gt 0 ]
    then
        echo -e "Following command launched on \e[1m$mac\e[0m on \e[3m$(date)\e[0m"
        echo "ssh hhours@$mac \"(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; python compute_node_link_overlap_from_list_version_20160531.py -i1 $FILETRN -i2 $FILETST -i3 $FILEUSR -on $FILEOUTNB -or $FILEOUTRN -ov $VECTFILE')\""
        if [ $debug -gt 1 ]
        then
            echo "Type enter to continue"
            read input
        fi
    fi
    if [ $debug -lt 3 ]
    then
        ssh hhours@$mac "(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; python compute_node_link_overlap_from_list_version_20160531.py -i1 $FILETRN -i2 $FILETST -i3 $FILEUSR -on $FILEOUTNB -or $FILEOUTRN -ov $VECTFILE')"
    fi

done 3< <(cat $listperiods)

rm $listmacs
