# *-* encoding: utf-8 *-*
import argparse,json,os,csv,sys,datetime,re,unicodedata,itertools

def parserTweetDate(filein,fileout_hsh,fileout_usrhsh,fileout_hshhsh,date):
    counter_sk = 0
    counter_notw = 0
    counter_ok = 0
    counter_line = 0

    for line in filein.readlines():
        counter_line += 1
        if counter_line % 100000 == 0:
            print(counter_line,'lines treated')
        try:
            tw = json.loads(line)
        except:
            counter_sk += 1
            continue
        if 'twitter' not in tw.keys():
            counter_notw += 1
            continue

        d = [int(i) for i in re.findall(r'[0-9]+',tw['twitter']['created_at'])]
        dt = datetime.datetime(*d[0:6])
        ts = dt.timestamp()

        if ts < date:
            if 'hashtags' in tw['twitter']:
                uid = tw['twitter']['user']['id']
                hashtags = tw['twitter']['hashtags']
                hashtags_f = []
                for h in hashtags:
                    h_f = ''.join(c for c in unicodedata.normalize('NFD', h) if unicodedata.category(c) != 'Mn').lower()
                    t = re.sub(r'[^a-zA-Z0-9]+','',h_f)
                    if t == h_f:
                        hashtags_f.append(h_f)
                        fileout_usrhsh.write(str(uid)+','+h_f+','+str(ts)+'\n')
                        fileout_hsh.write(h_f+','+str(ts)+'\n')
                if len(hashtags_f) > 1:
                    for el in itertools.combinations(hashtags_f,2):
                        fileout_hshhsh.write(el[0]+','+el[1]+','+str(ts)+'\n')
                        fileout_hshhsh.write(el[1]+','+el[0]+','+str(ts)+'\n')
            counter_ok+=1

    print('Finished treating file',filein.name,'for date',date)
    print(counter_line,'lines treated')
    print(counter_sk,'lines with no json format')
    print(counter_notw,'lines with no tweet format')
    print(counter_ok,'lines for which entries were created')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputfile',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Input file, json format, tweets")
    parser.add_argument('-o1','--outputHashes',
            type=argparse.FileType('a'),
            required=True,
            help="Output file for hash per period")
    parser.add_argument('-o2','--outputUserHashes',
            type=argparse.FileType('a'),
            required=True,
            help="Output file for user hash per period")
    parser.add_argument('-o3','--outputHashesHashes',
            type=argparse.FileType('a'),
            required=True,
            help="Output file for hash co occurences per period")
    parser.add_argument('-d','--date',
            type=float,
            required=True,
            help="Limit period (epoch time)")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    parserTweetDate(args.inputfile,args.outputHashes,args.outputUserHashes,args.outputHashesHashes,args.date)

    args.inputfile.close()
    args.outputHashes.close()
    args.outputUserHashes.close()
    args.outputHashesHashes.close()

if __name__ == '__main__':
    main()

 

