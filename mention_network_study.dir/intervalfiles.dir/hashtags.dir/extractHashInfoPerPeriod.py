# -*- encoding: utf-8 -*-
import os,sys,re,argparse,glob,csv

verbose=1

def parseFile(filein,fileout,date1,date2):
    counterline=0
    for line in filein:
        date = float(line.strip().split(',')[0])
        if date < date1:
            continue
        elif date > date2:
            if verbose > 0:
                print('Finished crawling file',filein.name)
                print(date,'>',date2)
                print(counterline,'added to output file',fileout.name)
            return
        else:
            counterline += 1
            fileout.write(line)
    if verbose > 0:
        print('End of file',filein.name)
        print(counterline,'added to output file',fileout.name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Path to month tweet hash")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file")
    parser.add_argument('-d1','--beginDate',
            type=float,
            required=True,
            help="epoch time of the beginning of the period")
    parser.add_argument('-d2','--endDate',
            type=float,
            required=True,
            help="epoch time of the finishing of the period")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    global verbose
    if args.output == sys.stdout:
        verbose=0

    parseFile(args.input,args.output,args.beginDate,args.endDate)
    args.input.close()
    args.output.close()
   
if __name__ == '__main__':
    main()
