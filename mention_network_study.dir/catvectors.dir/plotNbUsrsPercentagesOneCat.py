import matplotlib.pyplot as plt
import sys,os,csv,argparse


def plotPercNUsr(fileusr1,fileout,fileusr2,fileusr3,fileusr4):
    #remove header
    fileusr1.readline()
    lusr1 = list(csv.reader(fileusr1,delimiter=','))
    nusr = [int(el[0]) for el in lusr1]
    perc1 = [float(el[1]) for el in lusr1]



    nusr1 = len(lusr1)
    nusr2 = nusr1
    nusr3 = nusr1
    nusr4 = nusr1

    if fileusr2 != None:
        fileusr2.readline() 
        lusr2 = list(csv.reader(fileusr2,delimiter=','))
        nusr2 = len(lusr2)
        perc2 = [float(el[1]) for el in lusr2]
    if fileusr3 != None:
        fileusr3.readline()
        lusr3 = list(csv.reader(fileusr3,delimiter=','))
        nusr3 = len(lusr3)
        perc3 = [float(el[1]) for el in lusr3]
    if fileusr4 != None:
        fileusr4.readline()
        lusr4 = list(csv.reader(fileusr4,delimiter=','))
        nusr4 = len(lusr4)
        perc4 = [float(el[1]) for el in lusr4]
       
    
    if nusr1 != nusr2 or nusr2 != nusr3 or nusr3 != nusr4:
        print("Input size mistmatch, program will exit now")
        sys.exit(1)


    fig,ax1 = plt.subplots()
    ax1.bar(range(len(nusr)),nusr,alpha=0.4,color='b')
    ax1.set_xlabel('Increasing period',fontsize=18)
    ax1.set_ylabel('Number of users',fontsize=18)
    ax1.yaxis.label.set_color('b')
    for t1 in ax1.get_yticklabels():
            t1.set_color('b')
    ax2 = ax1.twinx()
    ax2.plot(range(len(nusr)),perc1,'r--',lw=1.5,marker='.',markersize=10,label='K = 20')
    if fileusr2 != None:
        ax2.plot(range(len(nusr)),perc2,'g--',lw=1.5,marker='*',markersize=10,label='K = 50')
    if fileusr3 != None:
        ax2.plot(range(len(nusr)),perc3,'b--',lw=1.5,marker='^',markersize=10,label='K = 100')
    if fileusr4 != None:
        ax2.plot(range(len(nusr)),perc3,'k--',lw=1.5,marker='v',markersize=10,label='K = 200')
    ax2.set_ylabel('Percentage of user with one category',fontsize=18)
    ax2.yaxis.label.set_color('k')
    plt.legend(fontsize=14,loc = 'upper left')
    for t1 in ax2.get_yticklabels():
            t1.set_color('k')
    plt.grid()
    plt.title('Percentage user in one cat\nNumber of clusters',fontsize=24,fontweight='bold')
    plt.tight_layout()
    plt.draw()
    plt.savefig(fileout)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1','--inputUsrK1',
            type = argparse.FileType('r'),
            required=True,
            help = "File storing percentage user with one cat with K = K1 <nusr,perc> (assume header)")
    parser.add_argument('-i2','--inputUsrK2',
            type = argparse.FileType('r'),
            required=False,
            default=None,
            help = "File storing percentage user with one cat with K = K2 <nusr,perc> (assume header) [OPTIONAL]")
    parser.add_argument('-i3','--inputUsrK3',
            type = argparse.FileType('r'),
            required=False,
            default=None,
            help = "File storing percentage user with one cat with K = K3 <nusr,perc> (assume header) [OPTIONAL]")
    parser.add_argument('-i4','--inputUsrK4',
            type = argparse.FileType('r'),
            required=False,
            default=None,
            help = "File storing percentage user with one cat with K = K4 <nusr,perc> (assume header) [OPTIONAL]")
    parser.add_argument('-o','--output',
            type = argparse.FileType('wb'),
            required=True,
            help = "File to save figure")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    plotPercNUsr(args.inputUsrK1,args.output,args.inputUsrK2,args.inputUsrK3,args.inputUsrK4)

    args.inputUsrK1.close()
    if args.inputUsrK2 != None:
        args.inputUsrK2.close()
    if args.inputUsrK3 != None:
        args.inputUsrK3.close()
    if args.inputUsrK4 != None:
        args.inputUsrK4.close()
    args.output.close()

if __name__ == '__main__':
    main()
