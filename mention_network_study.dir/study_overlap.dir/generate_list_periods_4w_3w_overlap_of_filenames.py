# *-* encoding: utf-8 *-*
import os,sys,csv,argparse

def generatelistFileName(filein,fileout):
    writer = csv.writer(fileout,delimiter=',',lineterminator=os.linesep)
    f1 = open(filein,'r')
    f2 = open(filein,'r')
    f2.readline()
    f2.readline()
    for l1 in f1.readlines():
        l2 = f2.readline()
        s1 = l1.strip()
        s2 = l2.strip()
        writer.writerow([s1,s2])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            required=True,
            help="List of consecutive,2 week 1 week overlap, filename period 'w1_w2'")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            required=True,
            help="Output file,csv, <w1_w2,w3_w4>, list period filename to build cumulative 4 weeks, 3 weeks overlap period of cumulative mentions")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    generatelistFileName(args.input,args.output)
    args.input.close()
    args.output.close()

if __name__ == '__main__':
    main()
