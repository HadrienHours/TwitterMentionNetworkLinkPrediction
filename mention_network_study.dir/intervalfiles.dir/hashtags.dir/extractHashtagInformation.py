# -*- coding: utf-8 -*-
import sys,json,re,unicodedata,string,argparse,csv,datetime

verbose=1

def extractHashTweet(filein,fileout):
    writer = csv.writer(fileout,delimiter=',')
    counter_err = 0
    counter_tw = 0
    counter_hsh = 0
    counter_hsh_alphanum = 0
    counter_notw = 0
    counter_line = 0
    counter_nodate = 0
    for entry in filein:
        counter_line += 1
        if counter_line % 1000000 == 0 and verbose > 0:
            print('Treating',counter_line,'th line')
        try:
            line = json.loads(entry)
        except:
            counter_err += 1
            continue
        if 'twitter' not in line.keys():
            counter_notw += 1
            continue

        cont = line['twitter']['text'].strip()

        if 'hashtags' in  line['twitter']:
            userID = line['twitter']['user']['id']
            counter_hsh += 1
            if 'created_at' not in line['twitter']:
                counter_nodate +=1
                continue
            d = [int(s) for s in re.findall(r'[0-9]+',line['twitter']['created_at'])]
            dt = datetime.datetime(*d[0:6])
            ts = dt.timestamp()
            hashtags = line['twitter']['hashtags']
            #remove hashtags
            for h in hashtags:
                pattern = re.compile('#'+h,re.IGNORECASE)
                cont = pattern.sub('',cont)
            #remove mentions
            if 'mentions' in line['twitter'].keys():
                for m in line['twitter']['mentions']:
                    pattern = re.compile('@'+m,re.IGNORECASE)
                    cont = pattern.sub('',cont)
            #remove links
            cont = re.sub(r'http[s]*://[^ \t,]+','',cont)
            #remove accent and to lower case
            cont = ''.join(c for c in unicodedata.normalize('NFD', cont) if unicodedata.category(c) != 'Mn').lower()
            #remove punctuation
            cont = cont.replace(',',' ').replace('.',' ').replace('!',' ').replace('?',' ').replace('/',' ')
            exclude = set(string.punctuation)
            cont = ''.join(s for s in cont if s not in exclude)
            listw = re.split('\s+',cont)
            listw = filter(lambda a: a == re.sub('[^a-zA-Z0-9]+','',a),listw)
            listw = filter(lambda a: a != '', listw)
            listw =  ' '.join(listw)
            hashtags_f = [''.join(c for c in unicodedata.normalize('NFD', h) if unicodedata.category(c) != 'Mn').lower() for h in hashtags]
            hashtags_f = [h for h in hashtags_f if h == re.sub('[^a-zA-Z0-9]+','',h)]
            if hashtags_f != [''] and listw  != ' ':
                for h in hashtags_f:
                    counter_hsh_alphanum += 1
                    writer.writerow([ts,userID,h,listw])
        counter_tw += 1

    
    if verbose > 0:
        print(counter_line,'lines treated')
        print(counter_tw,'tweets with right format')
        print(counter_hsh,'tweets with hashtag')
        print(counter_hsh_alphanum,'hashtag in alphanumeric format')
        print(counter_nodate,'tweet with no creation date')
        print(counter_notw,'no tweet format')
        print(counter_err,'no json format')

def main():
    parser = argparse.ArgumentParser(description="Crawler of json file, extract hashtag with time, ts and attached text")
    parser.add_argument('-i','--input',
            type = argparse.FileType('r'),
            default=sys.stdin,
            help="Input file, json format of tweets")
    parser.add_argument('-o','--output',
            type = argparse.FileType('w'),
            default = sys.stdout,
            help="Output file, csv format <ts,uid,hash,listwords> (only alphanumeric)")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    global verbose
    if args.output == sys.stdout:
        verbose=0

    extractHashTweet(args.input,args.output)

    args.input.close()
    args.output.close()

if __name__ == '__main__':
    main()
