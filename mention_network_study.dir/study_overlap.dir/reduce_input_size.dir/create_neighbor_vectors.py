# *-* encoding: utf-8 *-*
import argparse,os,sys,csv

verbose=1
debug=0
def createVectors(filein,fileout):

    writer = csv.writer(fileout,lineterminator=os.linesep,delimiter=",")

    counter_line=0

    d = {}


    for l in filein.readlines():
        counter_line += 1
        if counter_line % 100000 == 0 and verbose > 0:
            print('Treating line number:',counter_line)
        try:
            listv = [int(v) for v in l.strip().split(',')]
            uid = listv[0]
            mid = listv[1]
        except ValueError:
            if debug > 0 and verbose > 0:
                print('Following line had to be skipped (format)')
                print(l)
            continue

        if uid not in d:
            d[uid] = [mid]
        else:
            d[uid].append(mid)

        if mid not in d:
            d[mid] = [uid]
        else:
            d[mid].append(uid)

    for e in d:
        writer.writerow([e]+list(set(d[e])))

def main():
    parser = argparse.ArgumentParser(description="Create neighbor vectors from the list of observed mentions")
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Input file containing training mentions")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file, csv, first value user, rest its neighbors")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    global verbose
    if args.output == sys.stdout:
        verbose=0

    createVectors(args.input,args.output)
    args.input.close()
    args.output.close()

if __name__ == '__main__':
    main()
