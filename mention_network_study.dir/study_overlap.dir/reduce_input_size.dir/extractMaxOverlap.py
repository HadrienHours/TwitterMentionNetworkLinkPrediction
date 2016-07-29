# *-* encoding: utf-8 *-*
import argparse,sys,os,csv

verbose=1

def extractMax(filein,fileout):
    writer = csv.writer(fileout,lineterminator=os.linesep,delimiter=",")

    uid=0
    mid=0
    ovl=0

    for line in filein.readlines():
        listv=line.strip().split(',')
        try:
            uid_t = int(listv[0])
            mid_t = int(listv[1])
            ovl_t = float(listv[2])
        except ValueError:
            if verbose > 0:
                print('Following line was skipped, wrong format')
                print(line)
            continue

        if uid == uid_t and mid == mid_t:
            ovl=max(ovl,ovl_t)
        else:
            writer.writerow([uid,mid,ovl])
            uid=uid_t
            mid=mid_t
            ovl=ovl_t

    #last line
    writer.writerow([uid,mid,ovl])

def main():
    parser = argparse.ArgumentParser(description="From a list of mention with overlap, ordered, extract maximum for each unique mention")
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Input file:<uid,mid,overlap> ordered by uid,mid")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file:<uid,mid,overlap>, max overlap per {uid,mid}")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    global verbose
    if args.output == sys.stdout:
        verbose=0

    extractMax(args.input,args.output)

    args.input.close()
    args.output.close()

if __name__ == '__main__':
    main()
