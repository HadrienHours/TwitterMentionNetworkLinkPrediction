# *-* encoding: utf-8 *-*
# python computeOverlapNeighbor.py -i1 <(zcat $fileVectUserTrainInTest) -i2 <(zcat $listTestMention) -i3 <(zcat $listUserActivity) | gzip -c > $outNeighbor
import argparse,sys,os,csv

verbose=1
debug=0

def computeOverlap(dictVectors,fileMentions,listUserActivity,fileout):

    writer = csv.writer(fileout,lineterminator=os.linesep,delimiter=",")

    counterM = 0
    counter_sk = 0
    counter_read = 0
    counter_existing = 0
    counter_nouser=0

    writer.writerow(['user1','user2','overlap'])

    for line in fileMentions.readlines():
        counter_read += 1
        if counter_read % 10000 == 0 and verbose > 0:
            print(counter_read,'mentions studied')
            print(counterM,'overlaps computed')
            print(counter_existing,'already present')
            print(counter_nouser,'never seen before')
            print(counter_sk,'with 0 values, not present in training mention network')
            print('\n\n')

        if counterM % 10000 == 0 and verbose > 0:
            print(counterM,'overlaps computed')

        try:
            listv = [int(v) for v in line.strip().split(',')]
            uid=listv[0]
            mid=listv[1]
        except ValueError:
            if debug > 0 and verbose > 0:
                print('Following line skipped (wrong int format)')
                print(line)
            continue

        if (uid not in listUserActivity) or (mid not in listUserActivity):
            counter_nouser +=1
            continue

        try:
            nu = dictVectors[uid]
        except KeyError:
            writer.writerow([uid,mid,0])
            counter_sk += 1
            counterM +=1
            continue
        try:
            mu = dictVectors[mid]
        except KeyError:
            writer.writerow([uid,mid,0])
            counter_sk += 1
            counterM += 1
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
    parser.add_argument('-i2','--inputMentions',
            type=argparse.FileType('r'),
            required=True,
            help="List of testing mentions")
    parser.add_argument('-i3','--inputUserActivity',
            type=argparse.FileType('r'),
            required=True,
            help="List of user observed during the training period")
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
    listUserActivity = [int(line.strip()) for line in args.inputUserActivity.readlines()]
    
    computeOverlap(dictVectors,args.inputMentions,listUserActivity,args.output)

    args.inputVector.close()
    args.inputMentions.close()
    args.inputUserActivity.close()
    args.output.close()

if __name__ == '__main__':
    main()
