# -*- encoding: utf-8 -*-
import os,sys,re,argparse,csv

def parseFile(filein,dt,fileout):
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
        if date > dt:
            print('Finished crawling file',filein.name)
            print(date,'>',dt)
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
    listdates = [float(el[0]) for el in l1]
    for d in listdates:
        print('\n################################################################')
        print('\tStart extracting mention until date',d)
        print('################################################################\n')
        fileout=dirout+'/LISTMENTIONS_UNTIL_DATE_'+str(int(d))+'.csv'
        f = open(fileout,'w')
        parseFile(fileinput,d,f)
        f.close()
        fileinput.seek(0)
        print('\n################################################################')
        print('\tFinished parsing mentions till date ',d)
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
            help="csv file with period: <epochtime_endperiod>")
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
