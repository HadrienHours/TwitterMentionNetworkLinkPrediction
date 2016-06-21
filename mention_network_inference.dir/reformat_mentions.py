import os,sys,csv,re,argparse

def addDir(filein,fileout):
    counter = 0
    for line in filein:
        l = line.strip().split(',')
        uid = int(l[0])
        mid = int(l[1])
        if mid < uid:
            fileout.write(str(mid)+','+str(uid)+',1'+'\n')
        else:
            fileout.write(str(uid)+','+str(mid)+',0'+'\n')
        counter+=1
        if counter%1000000 == 0:
            print(counter,'lines treated')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",
            type = argparse.FileType("r"),
            default = sys.stdin,
            help="Input file")
    parser.add_argument("-o","--output",
            type = argparse.FileType("w"),
            default = sys.stdout,
            help="Output file")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    addDir(args.input,args.output)
    args.input.close()
    args.output.close()

if __name__ == "__main__":
    main()
