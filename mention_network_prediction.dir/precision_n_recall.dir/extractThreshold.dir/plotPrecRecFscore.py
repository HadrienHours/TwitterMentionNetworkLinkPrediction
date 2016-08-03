# *-* encoding: utf-8 *-*
import argparse,csv,sys,os
import matplotlib.pyplot as plt

def plotImprovement(listSim1,listSim2,listSim3,listSim4,listSim5,listSim6,lab1,lab2,lab3,lab4,lab5,lab6,fileout,tit,logf):
    X = range(len(listSim1))
    
    plt.figure()
    plt.plot(X,listSim1,'r--',lw=1.5,marker='*',markersize=12,label=lab1)
    if listSim2 != None:
        plt.plot(X,listSim2,'b--',lw=1.5,marker='x',markersize=12,label=lab2)
    if listSim3 != None:
        plt.plot(X,listSim3,'g--',lw=1.5,marker='^',markersize=12,label=lab3)
    if listSim4 != None:
        plt.plot(X,listSim4,'m--',lw=1.5,marker='v',markersize=12,label=lab4)
    if listSim5 != None:
        plt.plot(X,listSim5,'k--',lw=1.5,marker='H',markersize=12,label=lab5)
    if listSim6 != None:
        plt.plot(X,listSim6,'c--',lw=1.5,marker='o',markersize=12,label=lab6)
    if logf:
        plt.yscale('log')
    plt.grid()
    plt.legend(loc='lower center')
    plt.title(tit)
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
            help="Second input")
    parser.add_argument('-l2','--label2',
            type=str,
            help='legend second input')
    parser.add_argument('-i3','--input3',
            type=argparse.FileType('r'),
            help="Third input")
    parser.add_argument('-l3','--label3',
            type=str,
            help='legend third input')
    parser.add_argument('-i4','--input4',
            type=argparse.FileType('r'),
            help="Fourth input")
    parser.add_argument('-l4','--label4',
            type=str,
            help='legend fourth input')
    parser.add_argument('-i5','--input5',
            type=argparse.FileType('r'),
            help="Fifth input")
    parser.add_argument('-l5','--label5',
            type=str,
            help='legend fifth input')
    parser.add_argument('-i6','--input6',
            type=argparse.FileType('r'),
            help="Sixth input")
    parser.add_argument('-l6','--label6',
            type=str,
            help='legend sixth input')
    parser.add_argument('-d','--dim',
            type=int,
            required=True,
            help="Index dimension (starts at 0)")
    parser.add_argument('-o','--output',
            type=argparse.FileType('wb'),
            required=True,
            help="Output file")
    parser.add_argument('-t','--title',
            type=str,
            required=True,
            help="Plot title")
    parser.add_argument('--log',dest='logf',action='store_true',help="Set yscale in log")
    parser.set_defaults(logf=False)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()


    list1 = createList(args.input1,args.dim)
    if args.input2 != None:
        list2 = createList(args.input2,args.dim)
    else:
        list2 = None
    if args.input3 != None:
        list3 = createList(args.input3,args.dim)
    else:
        list3 = None
    if args.input4 != None:
        list4 = createList(args.input4,args.dim)
    else:
        list4 = None
    if args.input5 != None:
        list5 = createList(args.input5,args.dim)
    else:
        list5 = None
    if args.input6:
        list6 = createList(args.input6,args.dim)
    else:
        list6 = None

    plotImprovement(list1,list2,list3,list4,list5,list6,args.label1,args.label2,args.label3,args.label4,args.label5,args.label6,args.output,args.title,args.logf)

    args.input1.close()
    try:
        args.input2.close()
        args.input3.close()
        args.input4.close()
        args.input5.close()
        args.input6.close()
        args.output.close()
    except: 
        print('who cares')

if __name__ == '__main__':
    main()
