# -*- encoding: utf-8 -*-
import os,sys,re,argparse,glob,csv

def parseFile(filein,fileout,date1):
    counterline=0
    listv = list(csv.reader(filein,delimiter=','))
    for el in listv:
        date = float(el[-1])
        if date > date1:
            print('Finished crawling file',filein.name)
            print(date,'>',date1)
            print(counterline,'added to output file',fileout.name)
            return
        else:
            counterline += 1
            fileout.write(str(el[0])+','+str(el[1])+'\n')
    print('End of file',filein.name)
    print(counterline,'added to output file',fileout.name)

def parseDir(pathdir,fileout,date1):
    listfiles = glob.glob(pathdir+'/*.csv')
    for fn in listfiles:
        print('Start parsing file',fn,'for date',date1)
        f = open(fn,'r')
        parseFile(f,fileout,date1)
        f.close()

def parsePeriod(fileperiods,dirtweethash,dirout):
    for line in fileperiods.readlines():
        d1 = float(line.strip())
        print('\n################################################################')
        print('\tStart parsing user hashes for period finishing at ',d1)
        print('################################################################\n')
        fileout=dirout+'/userhashes_period_finishing_at_'+str(int(d1))+'.csv'
        f = open(fileout,'w')
        parseDir(dirtweethash,f,d1)
        f.close()
        print('\n################################################################')
        print('\tFinished parsing hashes for period till',d1)
        print('################################################################\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--pathDirUserHashes',
            type=str,
            required=True,
            help="Path to month user hash")
    parser.add_argument('-o','--pathDirOut',
            type=str,
            required=True,
            help="Path to store period tweets")
    parser.add_argument('-l','--listdates',
            type=argparse.FileType('r'),
            required=True,
            help="csv file with period: <epoch>")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if not os.path.isdir(args.pathDirUserHashes):
        print(args.pathDirTweets,"does not exist or not a directory")
        sys.exit(1)
    if not os.path.isdir(args.pathDirOut):
        print(args.pathDirOut,"does not exist or not a directory")
        sys.exit(1)

    parsePeriod(args.listdates,args.pathDirUserHashes,args.pathDirOut)
   
if __name__ == '__main__':
    main()
