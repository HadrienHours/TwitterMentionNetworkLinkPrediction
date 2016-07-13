#!/bin/bash

NARGS=4

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<inputdir><outputdir><login><listmachines>\n"
    tput sgr0
    exit 1
fi

debug=1

indir=$1
outdir=$2
user=$3
listm=$4

if [ ! -d $outdir ]
then
    mkdir -p $outdir
fi

listmacs=$(basename $listm | sed -re 's/\.[a-z]+$//1')_${RANDOM}.tsv

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
cwd=$(echo $cwdt | sed -re "s/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1")
dirout2=$(echo $outdir | sed -re "s/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1")

for filein in $indir/*.gz
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
    FILEIN=$(echo $filein | sed -re "s/\/media\/$user\//\/datastore\/complexnet\/test_hours\//1")
    FILEOUT=$dirout2/$(basename $filein | sed -re 's/\.gz//1')_RECIPROCAL_MENTIONS.gz

    if [ $debug -gt 1 ]
    then
        echo -e "ssh $user@$mac \"(cd $cwd && screen -d -m ./extract_reciprocal_mentions.sh $FILEIN $FILEOUT)\""
    else
        if [ $debug -gt 0 ]
        then
            echo -e "\n################################"
            echo "# On $mac ($env) at $(date)      #"
            echo -e "################################"
            echo -e "Extracting reciprocal mention for period file $(basename $filein)"
        fi
        ssh $user@$mac "(cd $cwd && screen -d -m ./extract_reciprocal_mentions.sh $FILEIN $FILEOUT)"
    fi
done

rm $listmacs
