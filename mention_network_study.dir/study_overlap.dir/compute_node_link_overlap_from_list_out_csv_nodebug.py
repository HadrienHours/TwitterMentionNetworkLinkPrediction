# *-* encoding: utf-8 *-*
import argparse,os,sys,csv,random

verbose=1

def create_neighbor_vectors(listNeighbors,fileoutVectors=None):

    if fileoutVectors != None:
        writer = csv.writer(fileoutVectors,lineterminator=os.linesep,delimiter=",")
    else:
        writer = None


    counter_line=0

    d_out = {}
    

    for l in listNeighbors.readlines():
        counter_line += 1
        if counter_line % 100000 == 0:
            print('Treating line number:',counter_line)
        try:
            listv = [int(v) for v in l.strip().split(',')]
            uid = listv[0]
            mid = listv[1]
        except ValueError:
            continue

        if uid not in d_out:
            d_out[uid] = [mid]
        else:
            d_out[uid].append(mid)

        if mid not in d_out:
            d_out[mid] = [uid]
        else:
            d_out[mid].append(uid)

    d_out2 = {}
    for e in d_out:
        d_out2[e] = list(set(d_out[e]))

        if writer != None:
            writer.writerow(e+d_out2[e])
    del d_out
    return d_out2

def computeOverlap(dneighbors,fileMentions,fileUsers,fileout):
    writer = csv.writer(fileout,lineterminator=os.linesep,delimiter=",")
    counterM = 0
    counter_sk = 0
    counter_read = 0
    counter_existing = 0
    counter_nouser=0

    
    listUsers = [int(user.strip()) for user in fileUsers.readlines()]

    writer.writerow(['user1','user2','overlap'])

    for line in fileMentions.readlines():
        counter_read += 1
        if counter_read % 10000 == 0:
            print(counter_read,'mentions studied')
            print(counterM,'overlaps computed')
            print(counter_existing,'already present')
            print(counter_nouser,'never seen before')
            print(counter_sk,'with 0 values, not present in training mention network')
            print('\n\n')

        if counterM % 10000 == 0:
            print(counterM,'overlaps computed')

        try:
            listv = [int(v) for v in line.strip().split(',')]
            uid=listv[0]
            mid=listv[1]
        except ValueError:
            continue

        if (uid not in listUsers) or (mid not in listUsers):
            counter_nouser +=1
            continue

        try:
            nu = dneighbors[uid]#.copy()
        except KeyError:
#            print('Error on ',counter_read,'testing mention')
#            print('Following entry not found in dict',uid)
#            if uid in dneighbors.keys():
#                print('Actually it is in')
#            input('Type enter to continue')
#
            writer.writerow([uid,mid,0])
            counter_sk += 1
            counterM +=1
            continue
        try:
            mu = dneighbors[mid]#.copy()
        except KeyError:
            writer.writerow([uid,mid,0])
            counter_sk += 1
            counterM += 1
            continue


        if (mid in nu) or (uid in mu):
            counter_existing +=1 
            continue

        #nu.append(mid)
        #mu.append(uid)

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
    return counterM,listUsers 

def computeOverlapRandom(dneighbors,nMentions,lUsers,fileout):
    print('Start computing average overlap, picking randomly ',nMentions,' couples of users')
    writer = csv.writer(fileout,lineterminator=os.linesep,delimiter=",")
    counter = 0

    thr = int(nMentions/100)+1

    perc = 0

    writer.writerow(['uid','mid','overlap'])

    nUsers = len(lUsers)-1

    while counter < nMentions:

        if counter%thr == 0:
            perc+=1
            print(perc,'% random overlaps computed')

        id1 = random.randint(0,nUsers)
        id2 = random.randint(0,nUsers)
        while id2 == id1:
            id2 = random.randint(0,nUsers)

        uid = lUsers[id1]
        mid = lUsers[id2]

        try:
            nu = dneighbors[uid]#.copy()
        except KeyError:
            writer.writerow([uid,mid,0])
            counter+=1
            continue

        try:
            mu = dneighbors[mid]#.copy()
        except KeyError:
            writer.writerow([uid,mid,0])
            counter += 1
            continue
        if (mid in nu) or (uid in mu):
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
            print('Mention id',mid,'with',kj,'neighbors')
            print('Number of common neighbors',nij)
            sys.exit(1)

        writer.writerow([uid,mid,overl])
        counter+=1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1','--trainingMentions',
            type = argparse.FileType('r'),
            required=True,
            help="List of mentions training, csvfile")
    parser.add_argument('-i2','--testingMentions',
            type=argparse.FileType('r'),
            required=True,
            help="List of mentions for testing")
    parser.add_argument('-i3','--listUsers',
            type=argparse.FileType('r'),
            required=True,
            help="List of users observed so far")
    parser.add_argument('-on','--outputOverlapNeighbor',
            type=argparse.FileType('w'),
            required=True,
            help="Output file, overlap for neighbors")
    parser.add_argument('-or','--outputOverlapRandom',
            type=argparse.FileType('w'),
            required=True,
            help="Output file, overlap for random nodes")
    parser.add_argument('-ov','--outputAdjVectors',
            type = argparse.FileType('w'),
            required=False,
            default=None,
            help="File storing each user adjacency vecors [OPTIONAL]")

    args = parser.parse_args()


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    d = create_neighbor_vectors(args.trainingMentions,args.outputAdjVectors)
    nc,lUsers = computeOverlap(d,args.testingMentions,args.listUsers,args.outputOverlapNeighbor)
    computeOverlapRandom(d,nc,lUsers,args.outputOverlapRandom)

    args.trainingMentions.close()
    args.testingMentions.close()
    args.listUsers.close()
    args.outputAdjVectors.close()
    args.outputOverlapNeighbor.close()
    args.outputOverlapRandom.close()

if __name__ == '__main__':
    main()
