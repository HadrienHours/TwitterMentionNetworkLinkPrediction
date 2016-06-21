# *-* encoding: utf-8 *-*
import argparse,csv,sys,os
import matplotlib.pyplot as plt

def plotImprovement(listSim1,listSim2,listSim3,lab1,lab2,lab3,fileout):
    X = range(len(listSim1))
    
    plt.figure()
    plt.plot(X,listSim1,'g--',lw=1.5,marker='o',markersize=12,label=lab1)
    plt.plot(X,listSim2,'r--',lw=1.5,marker='*',markersize=12,label=lab2)
    plt.plot(X,listSim3,'b--',lw=1.5,marker='^',markersize=12,label=lab3)
    plt.grid()
    plt.legend(loc='upper right')
    plt.draw()
    plt.savefig(fileout)
    plt.close()

def createList(filein,dim):
    #header
    filein.readline()

    listOut = [float(line.strip().split(',')[dim]) for line in filein]

    return listOut

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1','--input1',
            type=argparse.FileType('r'),
            required=True,
            help="First input")
    parser.add_argument('-l1','--label1',
            type=str,
            required=True,
            help='legend first input')
    parser.add_argument('-i2','--input2',
            type=argparse.FileType('r'),
            required=True,
            help="Second input")
    parser.add_argument('-l2','--label2',
            type=str,
            required=True,
            help='legend second input')
    parser.add_argument('-i3','--input3',
            type=argparse.FileType('r'),
            required=True,
            help="Third input")
    parser.add_argument('-l3','--label3',
            type=str,
            required=True,
            help='legend third input')
    parser.add_argument('-d','--dim',
            type=int,
            required=True,
            help="Index dimension (starts at 0)")
    parser.add_argument('-o','--output',
            type=argparse.FileType('wb'),
            required=True,
            help="Output file")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()


    list1 = createList(args.input1,args.dim)    
    list2 = createList(args.input2,args.dim)
    list3 = createList(args.input3,args.dim)

    plotImprovement(list1,list2,list3,args.label1,args.label2,args.label3,args.output)

    args.input1.close()
    args.input2.close()
    args.input3.close()
    args.output.close()

if __name__ == '__main__':
    main()
