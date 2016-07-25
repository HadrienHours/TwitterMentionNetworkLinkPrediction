# *-* encoding: utf-8 *-*
import argparse,os,sys,csv,random,subprocess

debug=1

def create_neighbor_vectors(listNeighbors):

    counter_line=0

    d_out = {}
    
    for l in listNeighbors.readlines():
        counter_line += 1
        if counter_line % 100000 == 0:
            print('Treating line number:',counter_line)
        try:
            uid = int(l.strip().split(',')[0])
            mid = int(l.strip().split(',')[1])
        except ValueError:
            if debug > 0:
                print('Following line had to be skipped (format)')
                print(l)
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
    del d_out
    return d_out2

def computeOverlap(dneighbors,fileout):
    counterU = 0
    counterC = 0

    print("gzip -c >",fileout)

    p = subprocess.Popen("gzip -c > "+fileout,shell=True,stdin=subprocess.PIPE)

    p.stdin.write('user1,user2,overlap\n'.encode('utf-8'))


    nUsers = len(dneighbors.keys())
    thr = int(nUsers/100)+1
    perc = 0

    shift=0
    for u1 in dneighbors:
        counterU+=1
        if debug > 1:
            print(str(counterU)+'th user being processed, uid = '+str(u1)+' (total:'+str(nUsers)+')')
        if counterU % thr == 0:
            perc+=1
            print(str(perc)+'% of users treated ('+str(counterU)+')')
            print(str(counterC)+' overlaps computed based on adjacency vectors')

        try:
            aL1 = dneighbors[u1]#.copy()
        except KeyError:
            continue
        for u2 in aL1:
            aL2 = dneighbors[u2]#.copy()
            for u3 in aL2:
                #If link exist, skip
                #To avoid computing twice overlap(u1,u3) = overlap(u3,u1), only compute if u3 > u1
                if (u3 <= u1) or u3 in aL1:
                    continue
                aL3 = dneighbors[u3]#.copy()

                o13 = getOverlap(u1,u3,aL1,aL3)
                s = str(u1)+','+str(u3)+','+str(o13)+'\n'
                p.stdin.write(s.encode('utf-8'))
                counterC+=1
                if counterC % 100000 ==0 :
                    print(str(counterC)+' overlaps computed')
    p.stdin.close()

def getOverlap(user1,user2,list1,list2):
        #list1.append(user2)
        #list2.append(user1)

        nij = len([n1 for n1 in list1 if n1 in list2])
        ki = len(list1)+1
        kj = len(list2)+1

        try:
            if nij == 0 and ki == kj == 1:
                return 0
            else:
                return float(nij)/float(ki - 1 + kj - 1 - nij)
        except ZeroDivisionError:
            print('Zero division error, program will exit')
            print('User id',user1,'with',ki,'neighbors')
            print('Mention id',user2,'with',kj,'neighbors')
            print('Number of common neighbors',nij)
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1','--trainingMentions',
            type = argparse.FileType('r'),
            required=True,
            help="List of mentions training, csvfile")
    parser.add_argument('-oo','--outputOverlap',
            type=str,
            required=True,
            help="Output file, overlap for non neighbors")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    d = create_neighbor_vectors(args.trainingMentions)
    print('Start computing overlaps')
    computeOverlap(d,args.outputOverlap)

    args.trainingMentions.close()

if __name__ == '__main__':
    main()
