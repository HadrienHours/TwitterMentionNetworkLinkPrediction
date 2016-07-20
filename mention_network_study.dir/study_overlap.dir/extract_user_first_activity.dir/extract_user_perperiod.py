# -*- encoding: utf-8 -*-
import os,sys,re,argparse,csv

verbose=1

def parseFile(filein,dt,fileout):
    counterline=0
    writer = csv.writer(fileout,delimiter=',',lineterminator=os.linesep)
    for line in filein.readlines():
        listv = line.strip().split(',')
        try:
            date = float(listv[1])
        except ValueError:
            if verbose > 0:
                print('Following line skipped (wrong format)')
                print(line)
            continue
        if date > dt:
            if verbose > 0:
                print('Finished crawling file',filein.name)
                print(date,'>',dt)
                print(counterline,'added to output file',fileout.name)
            return
        else:
            counterline += 1
            writer.writerow([listv[0]])
    if verbose > 0:
        print('End of file',filein.name)
        print(counterline,'added to output file',fileout.name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--listUserActivity',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="input file <epochtime,userID>")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file to store extracted userID")
    parser.add_argument('-d','--date',
            type=float,
            required=True,
            help="Epoch time marking the end of period")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    global verbose
    if args.output == sys.stdout:
        verbose = 0

    parseFile(args.listUserActivity,args.date,args.output)

    args.listUserActivity.close()
    args.output.close()
   
if __name__ == '__main__':
    main()
