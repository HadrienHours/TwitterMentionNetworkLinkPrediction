#!/bin/bash

NARGS=6
debug=1
renice=0
if [ $NARGS -ne $# ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<inputdir><outputdirhsh><outputdirusrhsh><outputhshsh><listdates><listmachines>$(tput sgr0)\n"
    exit 1
fi

dirin=$1
dirouthsh=$2
diroutusrhsh=$3
dirouthshhsh=$4
listdates=$5
listm=$6

if [ ! -d $dirouthsh ]
then
    mkdir -p $dirouthsh
fi

if [ ! -d $diroutusrhsh ]
then
    mkdir -p $diroutusrhsh
fi

if [ ! -d $dirouthshhsh ]
then
    mkdir $dirouthshhsh
fi


listmacs=${listm}_tmp

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

cwd=`pwd`
CWD=$(echo $cwd | sed -re 's/\/media\/hhours\//\/datastore\/complexnet\/test_hours\//1')
DIRIN=$(echo $dirin | sed -re 's/\/media\/hhours\//\/datastore\/complexnet\/test_hours\//1')
DIROUTHSH=$(echo $dirouthsh | sed -re 's/\/media\/hhours\//\/datastore\/complexnet\/test_hours\//1')
DIROUTUSRHSH=$(echo $diroutusrhsh | sed -re 's/\/media\/hhours\//\/datastore\/complexnet\/test_hours\//1')
DIROUTHSHHSH=$(echo $dirouthshhsh | sed -re 's/\/media\/hhours\//\/datastore\/complexnet\/test_hours\//1')

while read -u 3 dat
do
    #find a machine with no job running
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

    if [ $debug -eq 1 ]
    then
        echo "ssh hhours@$mac \"(cd $CWD && screen -d -m ./script_launch_one_period_crawler.sh $DIRIN $DIROUTHSH $DIROUTUSRHSH $DIROUTHSHHSH $dat)\""
    else
        echo -e "\n################################"
        echo "# On $mac ($env) at $(date)      #"
        echo -e "################################"
        echo "cmd launched ./script_launch_one_period_crawler.sh $DIRIN $DIROUTHSH $DIROUTUSRHSH $DIROUTHSHHSH $dt"
        ssh -n hhours@$mac "(cd $CWD && screen -d -m ./script_launch_one_period_crawler.sh $DIRIN $DIROUTHSH $DIROUTUSRHSH $DIROUTHSHHSH $dat)"
        if [  $renice -gt 0 ]
        then
            ssh -n hhours@$mac "renice -n 5 -u hhours"
        fi
    fi
    echo -e "\n\tCrawling for date $dat on machine $mac"
done 3< $listdates

rm $listmacs
