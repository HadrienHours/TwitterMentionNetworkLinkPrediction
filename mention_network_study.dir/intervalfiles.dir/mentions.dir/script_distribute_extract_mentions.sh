#!/bin/bash

NARGS=5

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<inputfile><outputdir><listtimes><user><listmachines>\n"
    tput sgr0
    exit 1
fi

debug=0

infile=$1
outdir=$2
listts=$3
user=$4
listm=$5

if [ ! -d $outdir ]
then
    mkdir -p $outdir
fi

listmacs=${listm}_tmp

if [ -f $listmacs ]
then
    rm $listmacs
fi

touch $listmacs

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

cwdt=`pwd`
cwd=$(echo $cwdt | sed -re 's/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1')
dirout2=$(echo $outdir | sed -re 's/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1')

while read -u 3 linedates
do
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
            sc=$(ssh -n $user@$mac "screen -ls" | grep -c -i "There is a screen on")
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
    d1=$(echo $linedates | cut -d , -f1)
    d2=$(echo $linedates | cut -d , -f2)
    d1n=$(echo $d1 | cut -d . -f1)
    d2n=$(echo $d2 | cut -d . -f1)
    OUTPUT=$dirout2/listmentions_period_${d1n}_${d2n}.csv
    INPUT=$(echo $infile | sed -re 's/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1')


    if [ $debug -eq 1 ]
    then
        echo -e "ssh $user@$mac \"(cd $cwd && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; \npython extract_mentions_interval_one_interval_20160331.py \n\t -i $INPUT \n\t-d1 $d1 \n\t-d2 $d2 \n\t-o $OUTPUT')\""
    else
        echo -e "\n################################"
        echo "# On $mac ($env) at $(date)      #"
        echo -e "################################"
        echo -e "cmd launched \n python extract_mentions_interval_one_interval_20160331.py -i $INPUT -d1 $d1 -d2 $d2 -o $OUTPUT"
        ssh $user@$mac "(cd $cwd && screen -d -m python extract_mentions_interval_one_interval_20160331.py -i $INPUT -d1 $d1 -d2 $d2 -o $OUTPUT)"

        #ssh $user@$mac "(cd $cwd && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; python extract_mentions_interval_one_interval_20160331.py -i $INPUT -d1 $d1 -d2 $d2 -o $OUTPUT')"
    fi
done 3< $listts

rm $listmacs
