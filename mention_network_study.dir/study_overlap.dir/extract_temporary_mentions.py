# -*- encoding: utf-8 -*-
import os,sys,re,argparse,csv

def parseFile(filein,d1,d2,fileout):
    counterline=0
    writer = csv.writer(fileout,delimiter=',',lineterminator=os.linesep)
    for line in filein.readlines():
        listv = line.strip().split(',')
        try:
            date = float(listv[0])
        except ValueError:
            print('Following line skipped (wrong format)')
            print(line)
            continue
        if date < d1:
            continue
        elif date > d2:
            print('Finished crawling file',filein.name)
            print(date,'>',d2)
            print(counterline,'added to output file',fileout.name)
            return
        else:
            counterline += 1
            writer.writerow([listv[1],listv[2]])
    print('End of file',filein.name)
    print(counterline,'added to output file',fileout.name)

def parsePeriod(fileinput,listDates,dirout):
    reader=csv.reader(listDates,delimiter=',')
    l1 = list(reader)
    listdates = [[float(el[0]),float(el[1])] for el in l1]
    for d in listdates:
        d1 = d[0]
        d2 = d[1]
        print('\n################################################################')
        print('\tStart extracting mention period',d1,'-',d2)
        print('################################################################\n')
        fileout=dirout+'/LISTMENTIONS_PERIOD_'+str(int(d1))+'-'+str(int(d2))+'.csv'
        f = open(fileout,'w')
        parseFile(fileinput,d[0],d[1],f)
        f.close()
        fileinput.seek(0)
        print('\n################################################################')
        print('\tFinished parsing mentions period',d1,'-',d2)
        print('################################################################\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--listMentions',
            type=argparse.FileType('r'),
            required=True,
            help="input file <epochtime,userID,mentionID>")
    parser.add_argument('-o','--pathDirOut',
            type=str,
            required=True,
            help="Path to dir to store extracted mentions")
    parser.add_argument('-l','--listDates',
            type=argparse.FileType('r'),
            required=True,
            help="csv file with period: <epochtime_beginperiod,epochtime_endperiod>")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if not os.path.isdir(args.pathDirOut):
        print(args.pathDirOut,"does not exist or not a directory")
        sys.exit(1)

    parsePeriod(args.listMentions,args.listDates,args.pathDirOut)

    args.listMentions.close()
    args.listDates.close()
   
if __name__ == '__main__':
    main()
