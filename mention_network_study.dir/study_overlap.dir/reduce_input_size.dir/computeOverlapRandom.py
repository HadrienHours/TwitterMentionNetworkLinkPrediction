# *-* encoding: utf-8 *-*
# python computeOverlapRandom.py -i1 <(zcat $fileVect) -i2 <(zcat $listUserActivity) -n $nU | gzip -c > $outRandom
import argparse,sys,os,csv,random

verbose=1
debug=0

def computeOverlap(dictVectors,listUserActivity,nMentions,fileout):
    writer = csv.writer(fileout,lineterminator=os.linesep,delimiter=",")

    nUsers=len(listUserActivity)-1

    thr=int(nMentions/100)+1
    perc=0
    
    counterM = 0
    counter_sk = 0
    counter_existing = 0
    counter_mentions = 0

    writer.writerow(['user1','user2','overlap'])


    while counterM < nMentions:
        counter_tried += 1
        if counter_tried % 10000 == 0 and verbose > 0:
            print(counter_tried,'mentions studied')
            print(counterM,'overlaps computed')
            print(counter_existing,'already present')
            print(counter_sk,'with 0 values, not present in training mention network')
            print('\n\n')

        if counterM % 10000 == 0 and verbose > 0:
            print(counterM,'overlaps computed')

        id1=random.randint(0,nUsers)
        id2=random.randint(0,nUsers)
        while id2 == id1:
            id2 = random.randinit(0,nUsers)

        uid = listUserActivity[id1]
        mid = listUserActivity[id2]

        try:
            nu = dictVectors[uid]
        except KeyError:
            writer.writerow([uid,mid,0])
            counter_sk += 1
            counterM +=1
            if counterM%thr == 0 and verbose > 0:
                perc+=1
                print(perc,'% random mentions computed (',counterM,'/',nMentions)
            continue
        try:
            mu = dictVectors[mid]
        except KeyError:
            writer.writerow([uid,mid,0])
            counter_sk += 1
            counterM += 1
            if counterM%thr==0 and verbose > 0:
                perc+=1
                print(perc,'% random mentions computed (',counterM,'/',nMentions)
            continue


        if (mid in nu) or (uid in mu):
            counter_existing +=1
            continue


        nij = len([n1 for n1 in nu if n1 in mu])
        ki = len(nu)+1
        kj = len(mu)+1

        try:
            if nij == 0 and ki == kj == 1:
                overl = 0
            else:
                overl = float(nij)/float(ki - 1 + kj - 1 - nij)
        except ZeroDivisionError:
            print('Zero division error, program will exit')
            print('User id',uid,'with',ki,'neighbors')
            print('List neighbors',nu)
            print('Mention id',mid,'with',kj,'neighbors')
            print('List neighbors',mu)
            print('Number of common neighbors',nij)
            sys.exit(1)

        writer.writerow([uid,mid,overl])
        counterM += 1

    if verbose > 0:
        print(counter_read,'tested mentions')
        print(counter_nouser,'skipped for user never seen')
        print(counterM,'overlaps computed')
        print(counter_sk,'skipped for no entries (',float(counter_sk)/float(counterM),'%)')
        print(counter_existing,'skipped for already present in training mention network')


def createDictVectors(filein):
    d = {}
    for line in csv.reader(filein):
        uid = int(line[0])
        neighbors = [int(el) for el in line[1:]]
        d[uid] = neighbors
    return d
    

def main():
    parser = argparse.ArgumentParser(description="Compute testing mention network user overlap based on the training mention network")
    parser.add_argument('-i1','--inputVector',
            type=argparse.FileType('r'),
            required=True,
            help="Input training mention neighbor vectors")
    parser.add_argument('-i2','--inputUserActivity',
            type=argparse.FileType('r'),
            required=True,
            help="List of user observed during the training period")
    parser.add_argument('-n','numberMentions',
            type=int,
            required=True,
            help="Number of random mentions to compute")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Ouput, overlap score per mention")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    global verbose
    if args.output == sys.stdout:
        verbose=0

    dictVectors = createDictVectors(args.inputVector)
    listMentions = [[int(el[0]),int(el[1])] for el in csv.reader(args.inputMentions,delimiter=",")]
    listUserActivity = [int(line.strip()) for line in args.inputUserActivity.readlines()]
    computeOverlap(dictVectors,listUserActivity,args.numberMentions,args.output)

    args.inputVector.close()
    args.inputMentions.close()
    args.inputUserActivity.close()
    args.output.close()

if __name__ == '__main__':
    main()
