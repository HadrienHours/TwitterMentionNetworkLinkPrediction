import sys,os,re,argparse,csv,numpy as np

verbose=1

def extractmentions(inputf,outputf,date1,date2):
    counterl = 0
    while True:
        l = inputf.readline().strip().split(',')
        t = float(l[2])
        if t > date1 and t < date2:
            counterl+=1
            uid = int(l[0])
            mid = int(l[1])
            if uid < mid:
                outputf.write(str(uid)+','+str(mid)+',0\n')
            else:
                outputf.write(str(mid)+','+str(uid)+',1\n')
        elif t > date2:
            if verbose > 0:
                print('Exiting for ',t,'bigger than',date2)
            break
    if verbose > 0:
        print(counterl,'mentions found for period [',date1,'-',date2,']')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",
            type=argparse.FileType("r"),
            default=sys.stdin,
            help="Input file in the format user1,user2,date(epoch): SORTED BY TIME")
    parser.add_argument("-o","--output",
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file in the format user1,user2,direction (user1<user2)")
    parser.add_argument('-d1','--date1',
            type=float,
            help='Date beginning interval (epoch)')
    parser.add_argument('-d2','--date2',
            type=float,
            help='Date ending interval (epoch)')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    global verbose
    if args.output == sys.stdout:
        verbose=0

    extractmentions(args.input,args.output,args.date1,args.date2)

    args.input.close()
    args.output.close()

if __name__ == "__main__":
    main()
