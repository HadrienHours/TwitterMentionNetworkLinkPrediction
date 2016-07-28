# *-* coding: utf-8 *-*
import os,sys,argparse,csv,random
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
verbose=1

def createVectorList(filein):
    listCatVectors = {}
    for line in filein:
        listv = line.strip().split(',')
        uid = int(listv[0])
        catV = [float(el) for el in listv[1:]]
        listCatVectors[uid] = catV
    return listCatVectors


def computeUserSimilarity(listMentions,listCatVectors,fileout):

    #remove header
    listMentions.readline()

    nV=0
    for line in listMentions.readlines():
        nV+=1

    listMentions.seek(0)

    thr=int(nV/100)+1
    counterU=0
    counterS=0
    perc=0


    fileout.write('user1,user2,cosineSimilarity\n')

    #remove header
    listMentions.readline()

    for line in listMentions.readlines():
        counterU+=1
        if counterU % thr == 0:
            perc+=1
            print(str(perc)+'% mentions treated, ('+str(counterU)+'/'+str(nV)+')')
            print(str(counterS)+' entries skipped for absence of categories for (at least) one user')

        listU = line.strip().split(',')
        u1 = int(listU[0])
        u2 = int(listU[1])
        

        try:
            c1 = listCatVectors[u1]
        except KeyError:
            counterS+=1
            continue

        try:
            c2 = listCatVectors[u2]
        except KeyError:
            counterS+=1
            continue

        s12 = cosine_similarity(c1,c2)[0][0]
        fileout.write(str(u1)+','+str(u2)+','+str(s12)+'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--listCatVectors',
            type=argparse.FileType('r'),
            help="file containing the list of category vectors in the format <uid,c1,.....,cn>")
    parser.add_argument('-m','--listMentions',
            type=argparse.FileType('r'),
            help="File containing the list of user couples in format <uid1,uid2>")
    parser.add_argument('-o','--outputFile',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file with similarity for each couple of users not already present in Mention Newtork")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    print('Building category list')
    listCatVectors = createVectorList(args.listCatVectors)
    print('Start computing user similarity')
    computeUserSimilarity(args.listMentions,listCatVectors,args.outputFile)

    args.listCatVectors.close()
    args.listMentions.close()
    args.outputFile.close()

if __name__ == '__main__':
    main()

