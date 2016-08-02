# *-* encoding: utf-8 *-*
import argparse,sys,os

def parseFile(filein,d1,d2):
    counter=0
    for line in filein.readlines():
        dt = float(line.strip().split(',')[1])
        if dt > d2:
            return counter
        if dt < d1:
            continue
        else:
            counter+=1
    return counter

def main():
    parser = argparse.ArgumentParser(description="Count number of tweets per period")
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Input file containing userId,Time(float), sorted chronologically !")
    parser.add_argument('-d1','--date1',
            type=float,
            default=0.0,
            help="Epoch time corresponding to beginning of period (default 0.0)")
    parser.add_argument('-d2','--date2',
            type=float,
            required=True,
            help="Epoch time corresponding to end of period")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file, store counter")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    counter = parseFile(args.input,args.date1,args.date2)

    if args.date1 == 0.0:
        args.output.write(str(args.date2)+','+str(counter)+'\n')
    else:
        args.output.write(str(args.date1)+'-'+str(args.date2)+','+str(counter)+'\n')

    args.input.close()
    args.output.close()

if __name__ == '__main__':
    main()
