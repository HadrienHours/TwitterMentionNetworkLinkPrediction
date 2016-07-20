# *-* encoding: utf-8 *-*
import os,sys,argparse

verbose=1

def extractUserFirstActivity(filein,fileout):
    counterLine=0
    counterUser=0
    current_uid = -1

    for l in filein.readlines():
        counterLine +=1
        if counterLine % 100000 and verbose > 0:
            print(counterLine,'lines treated')
        listv = l.strip().split(',')
        uid = int(listv[0])
        ts = int(float(listv[1]))
        if uid == current_uid:
            continue
        else:
            fileout.write(str(uid)+','+str(ts)+'\n')
            current_uid = uid
            counterUser+=1
            if counterUser % 10000 == 0 and verbose > 0:
                print(counterUser,'users treated')

    if verbose > 0:
        print('\n****\tFINISHED TREATING FILE\t***')
        print(counterLines,'lines treated')
        print(counterUser,'users treated')

def main():
    parser = argparse.ArgumentParser(description="Take stream of sorted user activity, select first time of activity")
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Input file in the format <uid,ts>, sorted by uid then ts")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file in the format <uid,ts>, only first uid ts")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    global verbose
    if args.output == sys.stdout:
        verbose=0

    extractUserFirstActivity(args.input,args.output)
    args.input.close()
    args.output.close()

if __name__ == '__main__':
    main()
