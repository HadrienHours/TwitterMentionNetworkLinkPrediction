#!/bin/bash

minNARGS=4
maxNARGS=7
debug=0

renice=0
if [ $# -lt $minNARGS ] ||  [ $# -gt $maxNARGS ]
then
    echo -e "\t\n$(tput bold)Usage $(basename $0):<dirinputfiles><diroutput><username><listmachines>[<minNeighbors><radius><minTweets>] (optional)\n"
    tput sgr0
    exit 1
fi

dirinp=$1
dirout=$2
user=$3
listm=$4

if [ $# -gt 4 ]
then
    minNeighbors=$5
fi
if [ $# -gt 5 ]
then
    radius=$6
    RADIUS=$(echo $radius | tr \. -)
fi
if [ $# -gt 6 ]
then
    minTweet=$7
fi

if [ -z $minNeighbors ]
then
    minNeighbors=2
fi

if [ -z $radius ]
then
    radius=0.7
    RADIUS=$(echo $radius | tr \. -)
fi

if [ -z $minTweets ]
then
    minTweets=10
fi

#Change, Random seed, for running several instance in parallel
listmacs=$(echo $listm | sed -re 's/\.tsv//1')_tmp_${RANDOM}.tsv

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

if [ $debug -lt 2 ]
then
    if [ -d $dirout ]
    then
        echo -e "$dirout already exists. Continue (risk of overwritting) [Y/N]:\t"
        read input
        if [ "$input" == "Y" ]
        then
            echo "ok"
        else
            exit 1
        fi
    else
        mkdir -p $dirout
    fi
fi

cwdt=`pwd`
cwd=$(echo $cwdt | sed -re 's/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1')
dirout2=$(echo $dirout | sed -re 's/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1')


nmacs=$(wc -l $listmacs | awk '{print $1}')
counter=1

for file in $dirinp/*.csv
do
    #find a machine with no job running
    flag_f=0
    while [ $flag_f -eq 0 ]
    do
        while IFS='' read -r line || [[ -n "$line" ]]
        do
            mac=$(echo $line | awk '{print $1}')
            env=$(echo $line | awk '{print $2}')
            if [ $debug -gt 0 ]
            then
                echo "Checking running screen on $mac"
            fi
            vl=$(ssh -o BatchMode=yes -n $user@$mac "uname -n")
            if [ -z $vl ]
            then
                continue
            fi
            sc=$(ssh -n $user@$mac "screen -ls" | grep -c -i "screen[s]* on")
            if [ $sc -eq 0 ]
            then
                if [ $debug -gt 0 ]
                then
                    echo "$mac found available"
                fi
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
    OUTPUT=$dirout2/$(basename $file | cut -d . -f1)_LABELS_DBSCAN_R_${RADIUS}_N_${minNeighbors}_T_${minTweets}.csv
    INPUT=$(echo $file | sed -re 's/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1')

    if [ $debug -gt 1 ]
    then
        echo "ssh $user@$mac \"(cd $cwd && screen -d -m bash -c 'source /datastore/complexnet/test_hours/conda_install.dir/install_dir/bin/activate dato-env; python clusterhashtweets.py -i $INPUT -o $OUTPUT -n $minNeighbors -r $radius -m $minTweets')\""
    else
        echo -e "\n################################"
        echo "# On $mac ($env) at $(date)      #"
        echo -e "################################"
        echo "cmd launched python clusterhashtweets.py -i $INPUT -o $OUTPUT -n $minNeighbors -r $radius -m $minTweets"
        ssh $user@$mac "(cd $cwd && screen -d -m bash -c 'source /datastore/complexnet/test_hours/conda_install.dir/install_dir/bin/activate dato-env; python clusterhashtweets.py -i $INPUT -o $OUTPUT -n $minNeighbors -r $radius -m $minTweets')"
        if [ $renice -gt 1 ]
        then
            ssh -n $user@$mac "renice -n 5 -u $user"
        fi
    fi
    echo -e "DBSCAN  with input $file on machine $mac\n"
done

rm $listmacs
