# *-* coding: utf-8 *-*
import os,sys,csv,argparse

def createListDate(date1,date2,step,overlap,fileout):
    writer = csv.writer(fileout,delimiter=',')
    step2=step-overlap
    d1 = date1
    d2 = date2
    while d1 < (date2 - step):
        d2 = d1 + step
        writer.writerow([d1,d2])
        d1 = d1+ step2
    

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-d1','--date1',
            type=float,
            help="First date (epoch)")
    parser.add_argument('-d2','--date2',
            type=float,
            help='Last date (epoch)')
    parser.add_argument('-s','--step',
            type=float,
            help='Length of each sub period (seconds)')
    parser.add_argument('-l','--overlap',
            type=float,
            help='Overlap (seconds)')
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            help='Output file')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.overlap > args.step:
        print('The overlap between two consecutive period cannot be bigger than the length of the period')
        sys.exit(1)

    createListDate(args.date1,args.date2,args.step,args.overlap,args.output)

    args.output.close()

if __name__ == '__main__':
    main()
