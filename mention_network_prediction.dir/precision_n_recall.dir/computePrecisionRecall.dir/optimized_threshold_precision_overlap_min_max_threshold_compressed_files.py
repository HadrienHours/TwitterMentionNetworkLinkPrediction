# *-* encoding: utf-8 *-*
import argparse,sys,os,csv

verbose=1

def findOptimalThreshold(filein,fileout,minT,maxT,step):
    writer = csv.writer(fileout,lineterminator=os.linesep,delimiter=',')
    writer.writerow(['threshold','TruePositive','FalsePositive','TrueNegative','FalseNegative','Precision','Recall'])

    listThresholds = [minT]
    val = minT
    while val < maxT:
        val+=step
        listThresholds.append(val)

    listScores = [[float(el[1]),bool(int(el[2]))] for el in csv.reader(filein,delimiter=',')]


    nThr = len(listThresholds)
    if nThr == 100:
        percT = 1
    else:
        percT = int(nThr/100)+1
    perc = 0
    counterThr = 0

    for thr in listThresholds:
        counterThr += 1
        if counterThr%percT == 0 and verbose > 0:
            perc+=1
            print(perc,'% threshold computed (',counterThr,'/',nThr,')')
        computePrecisionRecall(listScores,thr,writer)



def computePrecisionRecall(listScores,threshold,writer):
    counterTruePositive=0
    counterTrueNegative=0
    counterFalsePositive=0
    counterFalseNegative=0
    for el in listScores:
        if el[0] >= threshold:
            if el[1]:
                counterTruePositive +=1
            else:
                counterFalsePositive+=1
        else:
            if el[1]:
                counterFalseNegative+=1
            else:
                counterTrueNegative+=1
    if (counterTruePositive+counterFalsePositive) > 0:
        precision = float(counterTruePositive)/float((counterTruePositive+counterFalsePositive))
    else:
        precision = 0
    if (counterTruePositive+counterFalseNegative) > 0:
        recall = float(counterTruePositive)/float((counterTruePositive+counterFalseNegative))
    else:
        recall=0
    writer.writerow([threshold,counterTruePositive,counterFalsePositive,counterTrueNegative,counterFalseNegative,precision,recall])

def main():
    parser = argparse.ArgumentParser(description='compute precision and recall for different selection thresholds')
    parser.add_argument('-i','--input',
            type = argparse.FileType('r'),
            default=sys.stdin,
            help = "Input score file <uid-mid,score,selected(0/1)>")
    parser.add_argument('-m','--min',
            type = float,
            default = 0.1,
            help = "Minimum threshold to be tested (default 0.1)")
    parser.add_argument('-M','--max',
            type = float,
            default = 1.0,
            help = "Maximum threshold to be tested (default 0.1)")
    parser.add_argument('-s','--step',
            type = float,
            default = 0.1,
            help = "Step from 0 to 1 for thresholds to be tested (default 0.1)")
    parser.add_argument('-o','--output',
            type = argparse.FileType('w'),
            default=sys.stdout,
            help="output file")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    global verbose
    if args.output == sys.stdout:
        verbose=0

    findOptimalThreshold(args.input,args.output,args.min,args.max,args.step)
    args.input.close()
    args.output.close()

if __name__ == '__main__':
    main()
