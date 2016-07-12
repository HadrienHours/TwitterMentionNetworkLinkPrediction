#bzcat file.tgz | sed -re 's/^[^{]+//1' > python script -o output
import sys
import os
import argparse
import json
import datetime
import re
import time
verbose=1


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
                da = datetime.datetime(*d[0:6]) #convert date format
                if sys.version_info.major == 3:
                    dt = da.timestamp()
                elif sys.version_info.major == 2:
                    #dt.strftime('%s')
                    dt = time.mktime(da.timetuple())
                for mid in tweet['twitter']['mention_ids']:
                        if uid > mid:
                            fileoutput.write(str(mid)+','+str(uid)+','+str(1)+','+str(dt)+'\n')
                        else:
                            fileoutput.write(str(uid)+','+str(mid)+','+str(0)+','+str(dt)+'\n')
                        counter+=1
                if counter%10000 == 0:
                    print(counter,' lines added')

            except Exception as e:
                print(str(e))
                counter_skip_cr += 1
                continue

    #summary
    if verbose > 0:
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
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    global verbose
    if args.output == sys.stdout:
        verbose=0

    ids_dumped = parserperuser(args.input,args.output)
    args.input.close()
    args.output.close()

if __name__ == "__main__":
    main()
