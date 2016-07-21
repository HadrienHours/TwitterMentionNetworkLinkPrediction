# *-* coding: utf-8 *-*
import os,sys,argparse,csv,random,subprocess
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
verbose=1

def createVectorList(filein):
    listUserIds = []
    listCatVectors = []
    for line in filein:
        listv = line.strip().split(',')
        listUserIds.append(int(listv[0]))
        catV = [float(el) for el in listv[1:]]
        listCatVectors.append(catV)
    return (listUserIds,listCatVectors)

def createListUsers(fileUsers):
    listUsers = []
    for line in fileUsers:
        try:
            listv = [int(el) for el in line.strip().split(',')]
            listUsers.append(listv)
        except:
            print('Following line skipped (wrong format)')
            print(line)
    return listUsers

def computeUserSimilarity(listUsers,listCatVectors,listIndexes,fileout):
    #writer = csv.writer(fileout,delimiter=',')
    p = subprocess.Popen("gzip -c > "+fileout,shell=True,stdin=subprocess.PIPE)
    nV=len(listUsers)
    thr=int(nV/100)
    counter=0
    perc=0
    counterskip=0
    counterv=0
    ar = np.array([])
    for users in listUsers:
        counter+=1
        u1 = users[0]
        u2 = users[1]
        try:
            i1 = listIndexes.index(u1)
        except ValueError as e:
            if verbose > 1:
                print('No entry found for user',u1,' the mention ',u1,u2,'had to be skipped')
            counterskip+=1
            continue
        try:
            i2 = listIndexes.index(u2)
        except ValueError as e:
            if verbose > 1:
                print('No entry found for user',u2,' the mention ',u1,u2,'had to be skipped')
            counterskip += 1
            continue
        c1 = listCatVectors[i1]
        c2 = listCatVectors[i2]
        s12 = cosine_similarity(c1,c2)[0][0]
        ar_t = np.append(ar,s12)
        ar = ar_t
        del ar_t
        inp=str(u1)+','+str(u2)+','+str(s12)+'\n'
        p.stdin.write(inp.encode('utf-8'))
        counterv+=1
        if counter%thr == 0:
            perc+=1
            print(perc,'% done')
    print(counter,'lines treated')
    print(counterv,'mentions could be studied')
    print(counterskip,'mentions had to be skipped')
    m = ar.mean()
    s = ar.std()
    p.stdin.close()
    return (counterv,m,s)

def computeUserAverageSimilarity(listCatVectors,nSims,mM,sM,fileoutR,fileoutAvg):
    nC = len(listCatVectors)
    sims = np.zeros(nSims)
    count = 0
    p1 = subprocess.Popen("gzip -c > "+fileoutR,shell=True,stdin=subprocess.PIPE)
    p2 = subprocess.Popen("gzip -c > "+fileoutAvg,shell=True,stdin=subprocess.PIPE)

    s1 = 'uid,mid,cosine_similaritiy\n'
    p1.stdin.write(s1.encode('utf-8'))
    while count < nSims:
        u1 = random.randint(0,nC-1)
        u2 = random.randint(0,nC-1)
        c1 = listCatVectors[u1]
        c2 = listCatVectors[u2]
        sims[count] = cosine_similarity(c1,c2)[0][0]
        s1 = str(u1)+','+str(u2)+','+str(sims[count])+'\n'
        p1.stdin.write(s1.encode('utf-8'))
        count += 1
    p1.stdin.close()
    s1 = 'Type,Count,Average,Std\n'
    p2.stdin.write(s1.encode('utf-8'))
    s1 = 'Mentions,'+str(nSims)+','+str(mM)+','+str(sM)+'\n'
    p2.stdin.write(s1.encode('utf-8'))
    s1 = 'Random,'+str(count)+','+str(sims.mean())+','+str(sims.std())+'\n'
    p2.stdin.write(s1.encode('utf-8'))
    p2.stdin.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--listCatVectors',
            type=argparse.FileType('r'),
            help="file containing the list of category vectors in the format <uid,c1,.....,cn>")
    parser.add_argument('-u','--listUsers',
            type=argparse.FileType('r'),
            help="File containing the list of user couples in format <uid1,uid2>")
    parser.add_argument('-o1','--output1',
            type=str,
            required=True,
            help="Output file with similarity for each couple of users mentioning each other")
    parser.add_argument('-o2','--output2',
            type=str,
            required=True,
            help="Output file with similarity for couples of users randomly picked")
    parser.add_argument('-o3','--output3',
            type=str,
            required=True,
            help="Output file with average similarity and std")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    print('Extracting list of users')
    listUsers = createListUsers(args.listUsers)
    print('Building category list')
    listUserIds,listCatVectors = createVectorList(args.listCatVectors)
    print('Start computing user similarity')
    nS,mM,sM = computeUserSimilarity(listUsers,listCatVectors,listUserIds,args.output1)
    computeUserAverageSimilarity(listCatVectors,nS,mM,sM,args.output2,args.output3)

    args.listCatVectors.close()
    args.listUsers.close()

if __name__ == '__main__':
    main()

