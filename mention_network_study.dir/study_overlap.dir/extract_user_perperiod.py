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
            writer.writerow([listv[1]])
    print('End of file',filein.name)
    print(counterline,'added to output file',fileout.name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--listUserActivity',
            type=argparse.FileType('r'),
            required=True,
            help="input file <epochtime,userID>")
    parser.add_argument('-o','--dirOut',
            type=str,
            required=True,
            help="Path to dir to store extracted userID")
    parser.add_argument('-l','--listDates',
            type=argparse.FileType('r'),
            required=True,
            help="csv file with period: <epochtime_endperiod>")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if not os.path.isdir(args.dirOut):
        print(args.pathDirOut,"does not exist or not a directory")
        sys.exit(1)

    for line in args.listDates.readlines():
        dt = int(line.strip())
        fileout = args.dirOut+'/list_user_up_to_time_'+str(dt)+'.csv'
        fout = open(fileout,'w')
        parseFile(args.listUserActivity,float(dt),fout)
        fout.close()
        args.listUserActivity.seek(0)
        print('Finished parsing file',args.listUserActivity.name,'for date',dt)

    args.listUserActivity.close()
    args.listDates.close()
   
if __name__ == '__main__':
    main()
