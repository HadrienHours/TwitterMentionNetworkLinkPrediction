#!/bin/bash

minNARGS=6
maxNARGS=7
debug=1

if [ $# -lt $minNARGS ] || [ $# -gt $maxNARGS ]
then
    echo -e "\n\t\e[1mUsage $(basename $0):<dirinputtraining_4weeks><dirinputtesting_2weeks><dir_users><dirout><login><listmachines>[<banlist>]\e[0m\n"
    echo "List period:<period in filename training,period in filename testing>"
    echo -e "List mechine (tsv):<name_machine\tenvrionment\tnScreens>"
    echo -e "[Optional]: Ban list, training files not to process"
    exit 1
fi


dirintrn=$1
dirintst=$2
dirusers=$3
dirout=$4
userName=$5
listm=$6
if [ $# -eq $maxNARGS ]
then
    listBanFiles=$7
fi

auxdir=$dirout/aux.dir

if [ ! -d $auxdir ]
then
    mkdir -p $auxdir
fi

#Test machines
listmacs=$(echo $listm | sed -re 's/\.tsv//1')_${RANDOM}.tsv

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

DIRINTST=$(echo $dirintst | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")
DIRINTRN=$(echo $dirintrn | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")
DIRUSERS=$(echo $dirusers | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")
DIROUT=$(echo $dirout | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")
AUXDIR=$DIROUT/aux.dir
CWD=$(echo $(pwd) | sed -re "s/\/media\/$userName/\/datastore\/complexnet\/test_hours/1")

for filetrn in $dirintrn/*.tgz
do
    if [ ! -z $listBanFiles ]
    then
        fin=$(basename $filetrn)
        ban=$(cat $listBanFiles | grep $fin | wc -l | awk '{print $1}')
        if [ $ban -gt 0 ]
        then
            if [ $debug -gt 0 ]
            then
                echo "File $fin discarded (in ban file)"
                if [ $debug -gt 2 ]
                then
                    read input
                fi
            fi
            continue
        fi
    fi
    periodtrn=$(basename $filetrn | egrep -o "[0-9]{10}_[0-9]{10}")
    endTrn=$(echo $periodtrn | cut -d _ -f2)
    filetst=$(ls $dirintst/*.tgz | egrep "${endTrn}_")
    fileusr=$(ls $dirusers/*.tgz | egrep "${endTrn}")
    if [ -z $filetst ] || [ -z $fileusr ]
    then
        echo "Could not find files in $dirusers and $dirintst for file $filetrn, period $periodtrn (end period $endTrn), skipped"
        continue
    fi

    periodtst=$(basename $filetst | egrep -o "[0-9]{10}_[0-9]{10}")
    if [ -z $periodtst ]
    then
        echo "No testing period found in the filename $fileTst, period $periodtrn skipped"
        continue
    fi

    FILETRN=$DIRINTRN/$(basename $filetrn)
    FILETST=$DIRINTST/$(basename $filetst)
    FILEUSR=$DIRUSERS/$(basename $fileusr)

    #Find available machine
    if [ $debug -lt 2 ]
    then
        flag_f=0
        while [ $flag_f -eq 0 ]
        do
            while IFS='' read -r line || [[ -n "$line" ]]
            do
                mac=$(echo $line | awk '{print $1}')
                env=$(echo $line | awk '{print $2}')
                nSc=$(echo $line | awk '{print $3}')
                vl=$(ssh -o BatchMode=yes -n $userName@$mac "uname -n")
                if [ -z $vl ]
                then
                    continue
                fi
                ns=$(ssh -n $userName@$mac "screen -ls" | egrep -io "[0-9]+ socket" | egrep -o "[0-9]+")
                if [ -z $ns ]
                then
                    ns=0
                fi
                if [ $ns -lt $nSc ]
                then
                    flag_f=1
                    break
                fi
            done < <(cat $listmacs)
            if [ $flag_f -eq 0 ]
            then
                echo "All machines have been asigned max number of jobs, waiting 1 min before polling again"
                sleep 60
            fi
        done
    else
        mac=$(head -1 $listmacs | awk '{print $1}')
        env=$(head -1 $listmacs | awk '{print $2}')
    fi

    if [ $debug -gt 1 ]
    then
        echo "ssh $userName@$mac \"(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; ./script_compute_link_node_overlap.sh $FILETRN $FILETST $FILEUSR $DIROUT')\""
        if [ $debug -gt 2 ]
        then
            echo "Type enter to continue"
            read input
        fi
    else
        if [ $debug -gt 0 ]
        then
            echo -e "Launched on \e[1m$mac\e[0m on \e[3m$(date)\e[0m"
            echo "Computing overlap for period $periodtrn, inputs are $(basename $FILETRN), $(basename $FILETST), $(basename $FILEUSR)"
        fi
        ssh $userName@$mac "(cd $CWD && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; ./script_compute_link_node_overlap.sh $FILETRN $FILETST $FILEUSR $DIROUT')"
    fi
done 

rm $listmacs
