#*-* encoding: utf-8 *-*
import argparse,re,csv,json,sys,os,unicodedata,string

def parseFile(filein):
    counter_line = 0
    counter_notweet = 0
    counter_nojson = 0
    counter_noalphanumtw = 0
    counter_noalphanumhs = 0
    counter_mentions = 0
    max_mentions=0
    counter_hashtags = 0
    max_hashtags=0
    counter_links = 0
    max_links = 0
    list_count_mentions = []
    list_count_hashtags = []

    for line in filein.readlines():
        counter_line += 1
        if counter_line % 100000 == 0:
            print(counter_line,'lines parsed')
        try:
            tw = json.loads(line)
        except:
            counter_nojson += 1
            continue
        if 'twitter' not in tw:
            counter_notweet += 1
            continue
        cont = tw['twitter']['text'].strip()

        if 'hashtags' in tw['twitter']:
            hashtags = tw['twitter']['hashtags']
            for h in hashtags:
                pattern = re.compile('#'+h,re.IGNORECASE)
                cont = pattern.sub('',cont)
            hashtags_f = [''.join(c for c in unicodedata.normalize('NFD', h) if unicodedata.category(c) != 'Mn').lower() for h in hashtags]
            hashtags_f = [h for h in hashtags_f if h == re.sub('[^a-zA-Z0-9]+','',h)]
            if hashtags_f != ['']:
                counter_hashtags += 1
                nh = len(hashtags_f)
                while len(list_count_hashtags) < nh:
                    list_count_hashtags.append(0)
                list_count_hashtags[nh-1] += 1
                if nh > max_hashtags:
                    max_hashtags=nh
                    print('Following tweet with',nh,'hashtags')
                    print(tw['twitter']['text'])
                    print("##########################################\n\n")
                    print(tw)
                    print("##########################################\n\n")

            else:
                counter_noalphanumhs += 1
        #count and remove mentions
        if 'mentions' in tw['twitter'].keys():
            counter_mentions += 1
            nm = len(tw['twitter']['mentions'])
            while len(list_count_mentions) < nm:
                list_count_mentions.append(0)
            list_count_mentions[nm-1] += 1
            if nm > max_mentions:
                max_mentions=nm
                print('Following tweet with',nm,'mentions')
                print(tw['twitter']['text'])
                print("##########################################\n\n")
                print(tw)
                print("##########################################\n\n")


            for m in tw['twitter']['mentions']:
                pattern = re.compile('@'+m,re.IGNORECASE)
                cont = pattern.sub('',cont)
        #count and remove links
        prl = re.findall(r'http[s]*://[^ \t,]+',cont)
        if len(prl) > 0:
            counter_links += 1
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
        listw = ' '.join(listw.split()) #should replace several spaces with
        if len(listw) == 0:
            counter_noalphanumtw += 1
     

    #Print stats
    print(counter_line,'lines')
    print(counter_nojson,'with no json format')
    print(counter_notweet,'with no tweet format')
    print(counter_noalphanumtw,'tweets with no alpha numeric content')
    print(counter_links,'tweets with links')
    print(counter_hashtags,'tweets with hashtags')
    print(counter_noalphanumhs,'with non alphanumeric hashtags')
    print(counter_mentions,'tweets with mentions')
    counterm=0
    for l in list_count_mentions:
        counterm+=1
        print(list_count_mentions[counterm-1],'tweets with',counterm,'mentions')
    counterh=0
    for h in list_count_hashtags:
        counterh+=1
        print(list_count_hashtags[counterh-1],'tweets with',counterh,'hashtags')

def main():
    parser = argparse.ArgumentParser(description='Compute statistics for a set of tweets')
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Input file, tweets in JSON format")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    parseFile(args.input)
    args.input.close()

if __name__ == '__main__':
    main()

