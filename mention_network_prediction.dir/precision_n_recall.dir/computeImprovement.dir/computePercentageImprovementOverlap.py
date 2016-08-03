#*-* encoding: utf-8 *-*
import argparse,matplotlib.pyplot as plt,os,sys,csv

def computePercentage(listRef,listDest):
    outl = []
    for x,y in zip(listRef,listDest):
        try:
            perc = (y-x)/x
        except ZeroDivisionError:
            perc = 1

        outl.append(perc)
    return outl

def parseFile(filein):
    #remove header
    filein.readline()

    listPrec = []
    listRec = []
    listMean = []

    for line in filein.readlines():
        listv = line.strip().split(',')
        listPrec.append(float(listv[2]))
        listRec.append(float(listv[3]))
        listMean.append(float(listv[4]))
    return (listPrec,listRec,listMean)

def writeOutput(listPrec,listRec,listMean,fileout):
    writer = csv.writer(fileout,lineterminator=os.linesep,delimiter=',')
    writer.writerow(['precision','recall','harmonicMean'])
    for i in range(len(listPrec)):
        writer.writerow([listPrec[i],listRec[i],listMean[i]])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ir','--inputReference',
            type=argparse.FileType('r'),
            required=True,
            help="File with reference values <period,threshold,precision,recall,harmonicMean>")
    parser.add_argument('-ic','--inputCandidate',
            type=argparse.FileType('r'),
            required=True,
            help="File with candidate values <period,threshold,precision,recall,harmonicMean>")
    parser.add_argument('-o','--output',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="output file with % improvement,  <precision,recall,harmonicMean>")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    listPrecR,listRecR,listMeanR = parseFile(args.inputReference)
    listPrecC,listRecC,listMeanC = parseFile(args.inputCandidate)
    listPrec = computePercentage(listPrecR,listPrecC)
    listRec = computePercentage(listRecR,listRecC)
    listMean = computePercentage(listMeanR,listMeanC)

    writeOutput(listPrec,listRec,listMean,args.output)

    args.inputReference.close()
    args.inputCandidate.close()
    args.output.close()

if __name__ == '__main__':
    main()


