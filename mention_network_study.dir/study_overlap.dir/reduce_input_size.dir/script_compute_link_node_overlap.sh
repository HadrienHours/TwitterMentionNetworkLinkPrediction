#!/bin/bash

NARGS=4

if [ $# -ne $NARGS ]
then
    echo -e "Use of \e[1m$(basename $0)\e[0m:<fileTrainingMentions><fileTestingMentions><fileUserActivity><dirOut>\n"
    exit 1
fi

listTrainMention=$1
listTestMention=$2
listUserActivity=$3
dirOut=$4

auxdir=$dirOut/aux.dir
if [ ! -d $auxdir ]
then
    mkdir -p $auxdir
fi

start=$(date +%s)

trainPeriod=$(basename $listTrainMention | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")
testPeriod=$(basename $listTestMention | egrep -o "[0-9]{10}[_\-]{1}[0-9]{10}")

if [ -z $trainPeriod ] || [ -z $testPeriod ]
then
    echo "Could not find testing and training period in filename"
    exit 1
fi


#sort training and testing mention files along with listUserFile
fTsS1=$auxdir/TESTING_MENTIONS_PERIOD_${testPeriod}_SORTED_U1.tgz
fTsS2=$auxdir/TESTING_MENTIONS_PERIOD_${testPeriod}_SORTED_U2.tgz
fTrS=$auxdir/TRAINING_MENTIONS_PERIOD_${trainPeriod}_SORTED.tgz
fLU=$auxdir/LISTUSEROBSERVED_IN_TRAINING_PERIOD_${trainPeriod}_SORTED.tgz

zcat $listTrainMention | egrep -iv "id" | cut -d , -f1-2 | tr , "\n" | sort | uniq | gzip -c > $fTrS
zcat $listTestMention | egrep -iv "id" | sort -t , -k1,1 | gzip -c > $fTsS1
zcat $listTestMention | egrep -iv "id" | sort -t , -k2,2 | gzip -c > $fTsS2
zcat $listUserActivity | egrep -iv "id" | cut -d , -f1 | sort | uniq | gzip -c > $fLU
echo -e "\t\e[3mFinished sorting mentions and user files for periods\e[0m \e[1m$trainPeriod / $testPeriod\e[0m"


#select testing mentions for which uid and mid are in the training set
fTsS1Tr=$auxdir/TESTING_MENTIONS_PERIOD_${testPeriod}_UID_IN_TRAINING_PERIOD_${trainPeriod}.tgz
fTsS2Tr=$auxdir/TESTING_MENTIONS_PERIOD_${testPeriod}_MID_IN_TRAINING_PERIOD_${trainPeriod}.tgz
fOv=$auxdir/LIST_MENTIONS_TESTING_PERIOD_${testPeriod}_TOCOMPUTE.tgz
join -t , -11 <(zcat $fTsS1) -21 <(zcat $fTrS) | gzip -c > $fTsS1Tr
join -t , -12 <(zcat $fTsS2) -21 <(zcat $fTrS) | awk -F , 'BEGIN{OFS=","}{print $2,$1}' | gzip -c > $fTsS2Tr
zcat $fTsS1Tr $fTsS2Tr | sort | uniq -c | awk '{if($1==2){print $2}}' |gzip -c > $fOv
echo -e "\t\e[3mFinished selecting testing mentions of period \e[1m$testPeriod\e[3m in training mentions of period \e[1m$trainPeriod\e[0m"


#assign default 0 overlap for testing mentions including users observed in training period
fTsS1LU=$auxdir/TESTING_MENTIONS_PERIOD_${testPeriod}_UID_IN_USERS_OBSERVED_IN_PERIOD_${trainPeriod}.tgz
fTsS2LU=$auxdir/TESTING_MENTIONS_PERIOD_${testPeriod}_MID_IN_USERS_OBSERVED_IN_PERIOD_${trainPeriod}.tgz
f0Ov=$auxdir/TESTING_MENTIONS_PERIOD_${testPeriod}_USERS_OBSERVED_IN_PERIOD_${trainPeriod}_0_OVERLAP.tgz
join -t , -11 <(zcat $fTsS1) -21 <(zcat $fLU) | gzip -c > $fTsS1LU
join -t , -12 <(zcat $fTsS2) -21 <(zcat $fLU) | awk -F , 'BEGIN{OFS=","}{print $2,$1}' | gzip -c > $fTsS2LU
zcat $fTsS1LU $fTsS2LU | sort | uniq -c | awk 'BEGIN{OFS=","}{if($1==2){print $2,"0"}}' |gzip -c > $f0Ov
echo -e "\t\e[3mFinished assigning 0 overlap for testing mention of period \e[1m$testPeriod\e[0m\e[3m for which users have been observed in period \e[1m$trainPeriod\e[0m"


#Create training neighbor vectors
fileVect=$auxdir/NEIGHBOR_VECTOR_TRAINING_PERIOD_${trainPeriod}.tgz
python create_neighbor_vectors.py -i <(zcat $listTrainMention) | sort -t , -k1,1 | gzip -c > $fileVect
echo -e "\t\e[3mFinished creating neighbor vectors for training period \e[1m$trainPeriod\e[0m"

#Only select vectors for user present in testing mention network
fTsLu=$auxdir/LIST_USERS_IN_MENTION_NETWORK_TESTING_PERIOD_${testPeriod}.tgz
fileVectUserTrainInTest=$auxdir/NEIGHBOR_VECTOR_TRAINING_PERIOD_${trainPeriod}_USERS_IN_MENTION_NETWORK_TESTING_PERIOD_${testPeriod}.tgz
zcat $fOv | grep -iv "id" | tr , "\n" | sort | uniq | gzip -c > $fTsLu
join -t , -11 <(zcat $fileVect) -21 <(zcat $fTsLu) | gzip -c > $fileVectUserTrainInTest
echo -e "\t\e[3mFinished selecting neighbor vector minimum set of users for training period \e[1m$trainPeriod\e[0m"


#Compute neighbor overlap for user in training mention network
fNOv=$auxdir/TESTING_MENTIONS_PERIOD_${testPeriod}_USERS_IN_TRAINING_MENTION_NETWORK_PERIOD_${trainPeriod}.tgz
python computeOverlapNeighbor.py -i1 <(zcat $fileVectUserTrainInTest) -i2 <(zcat $fOv) -i3 <(zcat $listUserActivity) | gzip -c > $fNOv
echo -e "\t\e[3mFinished computing neighbor overlap for period \e[1m[$trainPeriod - $testPeriod]\e[0m"

#Merge zero and neighbor overlap files
outNeighbor=$dirOut/OVERLAP_TRAINING_PERIOD_${trainPeriod}_TESTING_PERIOD_${testPeriod}_NEIGHBOR.tgz
filein=$auxdir/LIST_ALL_OVERLAP_TESTING_PERIOD_${testPeriod}.tgz
zcat $fNOv $f0Ov | grep -iv "id" | sort -t , -k1,1 -k2,2 | gzip -c > $filein
python extractMaxOverlap.py -i <(zcat $filein) | gzip -c > $outNeighor
echo -e "\t\e[3m Finished merging training mention and observed users overlap for testing period \e[1m$testPeriod\e[0m"


#Compute random overlap
outRandom=$dirOut/OVERLAP_TRAINING_PERIOD_${trainPeriod}_TESTING_PERIOD_${testPeriod}_RANDOM.tgz
nU=$(zcat $outNeighbor | wc -l | awk '{print $1}')
python computeOverlapRandom.py -i1 <(zcat $fileVect) -i2 <(zcat $listUserActivity) -n $nU | gzip -c > $outRandom
echo -e "\t\e[1mFinished computing random overlap for period [$trainPeriod - $testPeriod]\e[0m"

finish=$(date +%s)

echo -e "\tTo treat period \e[3m$trainPeriod / $testPeriod\e[0m it took \e[1m$(( $finish-$start))s\e[0m"
