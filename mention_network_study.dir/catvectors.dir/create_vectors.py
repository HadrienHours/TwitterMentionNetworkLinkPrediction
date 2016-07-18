# *-* coding: utf-8 *-*
import argparse,sys,os,csv

verbose=1

def vectorizeStream(filein,fileout,nCats):
    writer = csv.writer(fileout,delimiter=',')
    counterl=0
    uid=-1
    cat=-1
    occ=-1
    sumv=0
    vect = [0 for i in range(nCats)]
    for line in filein.readlines():
        try:
            listv = line.strip().split(',')
            uid_c=int(listv[0])
            cat_c=int(listv[1])
            occ_c=int(listv[2])
        except ValueError as e:
            if verbose > 0:
                print('Wrong format, line below skipped')
                print(line)
            continue
        if uid == -1:
            uid=uid_c
            vect[cat_c]=float(occ_c)
            sumv+=occ_c
        elif uid_c != uid:
            vect = [el/sumv for el in vect]
            row = [uid]+vect
            writer.writerow(row)
            uid = uid_c
            vect = [0 for i in range(nCats)]
            vect[cat_c] = float(occ_c)
            sumv = occ_c
        else:
            vect[cat_c] = float(occ_c)
            sumv+= occ_c
        counterl+=1
        if counterl%1000 == 0 and verbose > 0:
            print(counterl,'lines treated')
    #write last line
    vect = [el/sumv for el in vect]
    row = [uid]+vect
    writer.writerow(row)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Input file in the format uid,cat,occurrence")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Output file in the format uid,nC0,...,nCk")
    parser.add_argument('-c','--nCats',
            type=int,
            help="Number of categories")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    global verbose
    if args.output == sys.stdout:
        verbose=0

    vectorizeStream(args.input,args.output,args.nCats)
    args.input.close()
    args.output.close()

if __name__ == '__main__':
    main()
