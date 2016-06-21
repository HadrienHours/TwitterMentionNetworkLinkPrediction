#!/bin/bash

NARGS=4

debug=2

if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<dirinput_sim><dirinput_men><diroutput><listperiods>\n$(tput sgr0)"
    exit 1
fi

dirinsim=$1
dirinmen=$2
dirout=$3
listperiods=$4

auxdir=$dirout/auxfiles.dir
vecdir=$dirout/neighborvectors.dir

if [ ! -d $auxdir ]
then
    mkdir -p $auxdir
fi

if [ ! -d $vecdir ]
then
    mkdir -p $vecdir
fi

while read -u 3 line
do
    period_sim=$(echo $line | cut -d , -f1)
    period_men=$(echo $line | cut -d , -f2)
    echo -e "Start treating period \e[1m${period_men}\e[0m with sim on period \e[1m${period_sim}\e[0m"
    
    filesim=$(ls $dirinsim | grep "$period_sim")
    filemen=$(ls $dirinmen | grep "$period_men")

    if [ -z $filesim ] || [ -z $filemen ]
    then
        echo "Could not find the testing and training files for periods ${period_sim} and ${period_men} in $dirinsim and $dirinmen, respectively"
        continue
    fi

    if [ $debug -gt 0 ]
    then
        echo -e "File mentions found is \e[3m${filemen}\e[0m"
        echo -e "File network found is \e[3m${filesim}\e[0m"
    fi
    fileran=$auxdir/LIST_RANDOM_MENTIONS_PERIOD_${period_men}.csv
    
    #Generate uniq list of users (for random)
    listusr=$auxdir/listusers_${period_men}.csv
    cat $dirinmen/$filemen | tr , "\n" | sort | uniq > $listusr

    #Generate all bidirectional mentions (for neighbor vectors)
    f1=$auxdir/$(basename $filesim | sed -re 's/\.csv//1')_BOTHDIRECTION_SORTED_USERID.csv
    ft=$auxdir/$(basename $filesim | sed -re 's/\.csv//1')_BOTHDIRECTION.csv
    f2=$vecdir/$(basename $filesim | sed -re 's/\.csv//1')_NEIGHBOR_VECTOR.csv
    f3=$dirout/SIMILARITY_FROM_MENTION_GRAPH_${period_sim}_NEIGHBOR_PERIOD_${period_men}_OVERLAP.csv
    f4=$vecdir/$(basename $filesim | sed -re 's/\.csv//1')_RANDOM_VECTOR.csv
    f5=$dirout/SIMILARITY_FROM_MENTION_GRAPH_${period_sim}_RANDOM_PERIOD_${period_men}_OVERLAP.csv
    cat $dirinsim/$filesim | sort -n -t , -k1,1 > $ft
    cat $dirinsim/$filesim | awk -F , 'BEGIN{OFS=","}{print $2,$1}' | sort -n -t , -k1,1 >> $ft
    cat $ft | sort -n -t , -k1,1 | sed '1iUserID,MentionID' > $f1
    echo -e "Finished sorting \e[3m $(basename $filesim)\e[0m, result stored in \e[3m$ft\e[0m"

    if [ $debug -gt 1 ]
    then
        echo "Type enter to continue"
        read input
    fi

    #Start computing overlap for neighbor at period M_i based on mention network at period P_i
    if [ $debug -gt 0 ]
    then
        echo -e "Cmd launched: \e[3mpython compute_node_link_overlap_from_list.py -i1 $dirinmen/$filemen -i2 $f1 -oc $f2 -oo $f3\e[0m"
    fi
    python compute_node_link_overlap_from_list.py -i1 $dirinmen/$filemen -i2 $f1 -oc $f2 -oo $f3

    if [ $debug -gt 0 ]
    then
        echo -e "Finished computing overlap for neighbors in mentions network at period ${period_men} based on mention network at period ${period_sim}"
        if [ $debug -gt 1 ]
        then
            echo "Type enter to continue"
            read input
        fi
    fi

    #Start computing overlap for random nodes from period M_i based on the mention network at period P_i
        #Generate list of random mentions
    nm=$(wc -l $dirinmen/$filemen | awk '{print $1}')
    python generaterandom_mentions.py -i $listusr -n $nm -o $fileran
    if [ $debug -gt 0 ]
    then
        echo "$nm random mentions generated and stored in $fileran"
    fi

    if [ $debug -gt 0 ]
    then
        echo -e "Cmd launched \e[3m python compute_node_link_overlap_from_list.py -i1 $fileran -i2 $f1 -oc $f4 -oo $f5\e[0m"
    fi
    python compute_node_link_overlap_from_list.py -i1 $fileran -i2 $f1 -oc $f4 -oo $f5
    echo -e "Finished treating \e[3m $(basename $filesim), $(basename $filemen)\e[0m, result stored in \e[3m$f3\e[0m"
done 3< <(cat $listperiods)
