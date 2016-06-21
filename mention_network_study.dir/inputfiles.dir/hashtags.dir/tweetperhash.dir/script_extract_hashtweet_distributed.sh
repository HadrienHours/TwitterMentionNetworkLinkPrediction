#!/bin/bash

NARGS=4

debug=1
if [ $# -ne $NARGS ]
then
    echo -e "\n\t$(tput bold)Usage $(basename $0):<fileinput><fileouput><machine><env>\n$(tput sgr0)"
    echo "Input file: tgz month file"
    echo "Ouput file:  csv file:<epoch,hash,listwords>"
    echo "machine: ssh w/o passwd"
    echo "env: hadrien2/hadrien3"
    exit 1
fi

filein=$(echo $1 | sed -re 's/\/media\/hhours/\/datastore\/complexnet\/test_hours/1')
fileout=$(echo $2 | sed -re 's/\/media\/hhours/\/datastore\/complexnet\/test_hours/1')
mac=$3
env=$4

if [ "$env" == "hadrien2" ]
then
    pathenv=/datastore/complexnet/test_hours/hadrien2/bin/activate
elif [ "$env" == "hadrien3" ]
then
    pathenv=/datastore/complexnet/test_hours/hadrien3/bin/activate
else
    echo "Wrong environment (hadrien2/hadrien3)"
    exit 1
fi

res=$(ssh -n -o BatchMode=yes hhours@$mac "uname -n")
if [ -z $res ]
then
    echo "machine $mac seem not reachable"
    exit 1
fi

cwdt=`pwd`
cwd=$(echo $cwdt | sed -re 's/\/media\/hhours\//\/datastore\/complexnet\/test_hours\//1')

if [ $debug -gt 0 ]
then
    echo -e "\n################################"
    echo "# On $mac ($env) at $(date)      #"
    echo -e "################################"
    echo "ssh hhours@$mac \"(cd $cwd && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; zcat $filein | python extracthashtweets.py -o $fileout')\""
fi

if [ $debug -lt 2 ]
then
    ssh hhours@$mac "(cd $cwd && screen -d -m bash -c 'source /datastore/complexnet/test_hours/$env/bin/activate; zcat $filein | python extracthashtweets.py -o $fileout')"
fi
