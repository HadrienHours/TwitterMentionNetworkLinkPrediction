# *-* coding: utf-8 *-*
import os,sys,argparse,csv,random
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
    writer = csv.writer(fileout,delimiter=',')
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
        writer.writerow([u1,u2,s12])
        counterv+=1
        if counter%thr == 0:
            perc+=1
            print(perc,'% done')
    print(counter,'lines treated')
    print(counterv,'mentions could be studied')
    print(counterskip,'mentions had to be skipped')
    m = ar.mean()
    s = ar.std()
    return (counterv,m,s)

def computeUserAverageSimilarity(listCatVectors,nSims,mM,sM,fileoutR,fileoutAvg):
    nC = len(listCatVectors)
    sims = np.zeros(nSims)
    count = 0
    writer1 = csv.writer(fileoutR,delimiter=',',lineterminator=os.linesep)
    writer2 = csv.writer(fileoutAvg,delimiter=',',lineterminator=os.linesep)
    writer1.writerow(['uid','mid','cosine_similarit'])
    while count < nSims:
        u1 = random.randint(0,nC-1)
        u2 = random.randint(0,nC-1)
        c1 = listCatVectors[u1]
        c2 = listCatVectors[u2]
        sims[count] = cosine_similarity(c1,c2)[0][0]
        writer1.writerow([u1,u2,sims[count]])
        count += 1
    writer2.writerow(['Type','Count','Average','Std'])
    writer2.writerow(['Mentions',nSims,mM,sM])
    writer2.writerow(['Random',count,sims.mean(),sims.std()])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--listCatVectors',
            type=argparse.FileType('r'),
            help="file containing the list of category vectors in the format <uid,c1,.....,cn>")
    parser.add_argument('-u','--listUsers',
            type=argparse.FileType('r'),
            help="File containing the list of user couples in format <uid1,uid2>")
    parser.add_argument('-o1','--output1',
            type=argparse.FileType('w'),
            help="Output file with similarity for each couple of users mentioning each other")
    parser.add_argument('-o2','--output2',
            type=argparse.FileType('w'),
            help="Output file with similarity for couples of users randomly picked")
    parser.add_argument('-o3','--output3',
            type=argparse.FileType('w'),
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

    args.output1.close()
    args.output2.close()
    args.output3.close()
    args.listCatVectors.close()

if __name__ == '__main__':
    main()

