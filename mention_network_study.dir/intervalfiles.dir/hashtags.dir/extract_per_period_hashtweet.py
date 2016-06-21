# -*- encoding: utf-8 -*-
import os,sys,re,argparse,glob,csv

def parseFile(filein,fileout,date1,date2):
    counterline=0
    for line in filein:
        date = float(line.strip().split(',')[0])
        if date < date1:
            continue
        elif date > date2:
            print('Finished crawling file',filein.name)
            print(date,'>',date2)
            print(counterline,'added to output file',fileout.name)
            return
        else:
            counterline += 1
            fileout.write(','.join(line.strip().split(',')[1:]))
            fileout.write('\n')
    print('End of file',filein.name)
    print(counterline,'added to output file',fileout.name)

def parseDir(pathdir,fileout,date1,date2):
    listfiles = glob.glob(pathdir+'/*.csv')
    for fn in listfiles:
        print('Start parsing file',fn,'for dates',date1,'-',date2)
        f = open(fn,'r')
        parseFile(f,fileout,date1,date2)
        f.close()

def parsePeriod(fileperiods,dirtweethash,dirout):
    reader=csv.reader(fileperiods,delimiter=',')
    l1 = list(reader)
    listdates = [[float(el[0]),float(el[1])] for el in l1]
    for d in listdates:
        d1 = d[0]
        d2 = d[1]
        print('\n################################################################')
        print('\tStart parsing tweets for period ',d1,'-',d2)
        print('################################################################\n')
        fileout=dirout+'/tweet_per_hash_period_'+str(int(d1))+'-'+str(int(d2))+'.csv'
        f = open(fileout,'w')
        parseDir(dirtweethash,f,d1,d2)
        f.close()
        print('\n################################################################')
        print('\tFinished parsing tweets for period ',d1,'-',d2)
        print('################################################################\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--pathDirTweets',
            type=str,
            required=True,
            help="Path to month tweet hash")
    parser.add_argument('-o','--pathDirOut',
            type=str,
            required=True,
            help="Path to store period tweets")
    parser.add_argument('-l','--listdates',
            type=argparse.FileType('r'),
            required=True,
            help="csv file with period: <epoch1,epoch2>")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if not os.path.isdir(args.pathDirTweets):
        print(args.pathDirTweets,"does not exist or not a directory")
        sys.exit(1)
    if not os.path.isdir(args.pathDirOut):
        print(args.pathDirOut,"does not exist or not a directory")
        sys.exit(1)

    parsePeriod(args.listdates,args.pathDirTweets,args.pathDirOut)
   
if __name__ == '__main__':
    main()
