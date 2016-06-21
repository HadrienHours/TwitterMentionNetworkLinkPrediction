#bzcat file.tgz | sed -re 's/^[^{]+//1' > python script -o output
import sys
import os
import argparse
import json
import datetime
import re
verbose=0
pversion=2

def printtweetinfos(input, output):
    flagline=0
    maxC=10
    counter=0
    for line in input:
        tweet = json.loads(line)
        if 'mention_ids' in tweet['twitter'].keys():
            counter+=1
            print('\n\n')
            if flagline == 1:
                print("##########################")
                print("####      LINE        ####")
                print("##########################")
                print(line)
            print("##########################")
            print("####      TWEET       ####")
            print("##########################")
 #           print(tweet['twitter'])
            print("tweet['twitter']['user']['id'] :",tweet['twitter']['user']['id'])
            print("tweet['twitter']['created_at'] :",tweet['twitter']['created_at'])
            print("tweet['twitter']['mention_ids'] :",tweet['twitter']['mention_ids'])
            if counter >= maxC:
                return 0

def parserperuser(fileinput,fileoutput):
    counter=0
    counter_skip_tw = 0
    counter_skip_cr = 0
    for line in fileinput:
        try:
            tweet = json.loads(line)
        except Exception as e:
            counter_skip_cr += 1
            continue
        if 'twitter' not in tweet.keys():
            counter_skip_tw +=1
            continue
        if 'mention_ids' in tweet['twitter'].keys():
            try:
                uid = tweet['twitter']['user']['id']
                d = [int(s) for s in re.findall(r'[0-9]+',tweet['twitter']['created_at'])] #Get only numbers
                da = str(datetime.datetime(*d[0:6])) #convert date format
                for m in tweet['twitter']['mention_ids']:
                        json.dump({'user_id':uid,'mention_id':m,'date':da},fileoutput)
                        fileoutput.write('\n')
                        counter+=1
                if counter%10000 == 0:
                    print(counter,' lines added')

            except Exception as e:
                print(str(e))
                counter_skip_cr += 1
                continue

    #summary
    print(counter,' lines treated')
    print(counter_skip_tw,' entries not treated for not containing tweets')
    print(counter_skip_cr,' entries not treated for wrong format')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--input",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="input file name")
    parser.add_argument("-o","--output",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="mms output")
    parser.add_argument("-v","--verbose",
            type=int,
            default=0,
            help="verbose level: None (0), Quiet (1), Verbosy (2)")
    args = parser.parse_args()
    global verbose
    verbose = args.verbose
    global pversion
    pversion=sys.version.split('.')[0]
    ids_dumped = parserperuser(args.input,args.output)
    args.input.close()
    args.output.close()

if __name__ == "__main__":
    main()
