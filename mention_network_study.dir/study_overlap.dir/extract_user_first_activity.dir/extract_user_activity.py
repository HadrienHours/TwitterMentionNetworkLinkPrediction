# *-* encoding: utf-8 *-*
import json,sys,os,re,argparse,datetime,csv

verbose=1

def parseTweetFile(filein,fileout):
    counter_nojs = 0
    counter_notw = 0
    counter_line = 0

    for line in filein.readlines():
        counter_line +=1
        if counter_line %100000 == 0 and verbose > 0:
            print(counter_line,'lines treated')
        try:
            tw = json.loads(line)
        except:
            counter_nojs +=1
            continue

        if 'twitter' not in tw:
            counter_notw += 1
            continue

        uid = int(tw['twitter']['user']['id'])
        d = [int(s) for s in re.findall(r'[0-9]+',tw['twitter']['created_at'])]
        dt = datetime.datetime(*d[0:6])
        ts = dt.timestamp()
        fileout.write(str(uid)+','+str(ts)+'\n')

    if verbose > 0:
        print(counter_lines,'lines parsed')
        print(counter_nojs,'lines in a non json format')
        print(counter_notw,'lines in a non twitter format')


def main():
    parser = argparse.ArgumentParser(description="Parse Json files containing tweets, extract user ID and time of activity")
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Input file, json format, containing tweets")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file, csv format, containing <userID,ts>")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    global verbose
    if args.output == sys.stdout:
        verbose = 0

    parseTweetFile(args.input,args.output)

    args.input.close()
    args.output.close()

if __name__ == '__main__':
    main()
        
