import sys,os,re,argparse,csv,numpy as np
import pandas as pd

full_mention = 1

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
            print('Exiting for ',t,'bigger than',date2)
            break
    print(counterl,'mentions found for period [',date1,'-',date2,']')

def extractMentionLists(inputfile,fileDates,outputdir):
    reader = csv.reader(fileDates,delimiter=',')
    for line in reader:
        d1 = float(line[0])
        d2 = float(line[1])
        d1n = str(int(d1))
        d2n = str(int(d2))
        outputname = outputdir+'/listmentions_period_'+d1n+'-'+d2n+'.csv'
        outputf = open(outputname,'w')
        inputfile.seek(0)
        extractmentions(inputfile,outputf,d1,d2)
        #print('Finish extracting mentions for the period ['+d1n+'-'+d2n+']')
        print('Saved as',outputname)
        outputf.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",
            type=argparse.FileType("r"),
            default=sys.stdin,
            help="Input file in the format user1,user2,date(epoch): SORTED BY TIME")
    parser.add_argument("-o","--outputdir",
            type=str,
            help="Output directory to store files in the format user1,user2,direction")
    parser.add_argument('-l','--listdates',
            type=argparse.FileType('r'),
            help='List dates (epoch) <begining,end> of the periods')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if os.path.exists(args.outputdir):
        print(args.outputdir,'already exists.')
        if sys.version_info.major == 3:
            choice = input('Still use as target dir ? [Y/N]:\t')
        else:
            choice = raw_input('Still use as target dir ? [Y/N]:\t')
        if choice == 'Y':
            print('Ok (overwrite possible)')
        else:
            sys.exit(1)
    else:
        os.mkdir(args.outputdir)

    extractMentionLists(args.input,args.listdates,args.outputdir)
    args.input.close()
    args.listdates.close()

if __name__ == "__main__":
    main()
