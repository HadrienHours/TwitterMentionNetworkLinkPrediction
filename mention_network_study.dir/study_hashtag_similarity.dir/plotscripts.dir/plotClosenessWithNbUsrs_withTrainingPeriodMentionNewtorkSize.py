import matplotlib.pyplot as plt
import sys,os,csv,argparse


def plotSimNUsr(fileoverlap,fileout,tit,log):
    #remove header
    fileoverlap.readline()
    listoverlaps = list(csv.reader(fileoverlap,delimiter=','))
    listoverlaps1 = []
    for el in listoverlaps:
        listoverlaps1.append([float(el2) for el2 in el[1:]])
    listNTraining = [int(el[0]) for el in listoverlaps1 ]
    listNTesting = [int(el[1]) for el in listoverlaps1]
    listoverlap_mention = [el[2] for el in listoverlaps1]
    listoverlap_random = [el[3] for el in listoverlaps1]

    fig,ax1 = plt.subplots()
    ax1.bar(range(len(listNTraining)),listNTraining,alpha=0.4,color='b')
    ax1.set_xlabel('Increasing period',fontsize=24)
    ax1.set_ylabel('Number of mentions',fontsize=24)
    #if log:
    ax1.set_yscale('log')
    ax1.yaxis.label.set_color('b')
    for t1 in ax1.get_yticklabels():
            t1.set_color('b')
    #ax2 = ax1.twinx()
    ax1.bar(range(len(listNTesting)),listNTesting,alpha=0.6,color='b')

    ax3 = ax1.twinx()
    ax3.plot(range(len(listoverlaps1)),listoverlap_mention,'r--',lw=1.5,marker='*',markersize=10,label='Closeness mention neighbors')
    ax3.plot(range(len(listoverlaps1)),listoverlap_random,'r--',lw=1.5,marker='.',markersize=12,label='Closeness random nodes')
    ax3.set_ylabel('Average closeness for users',fontsize=24)
    if log:
        ax3.set_yscale('log')
    ax3.yaxis.label.set_color('r')
    plt.legend(fontsize=12,loc = 'center left')
    for t1 in ax3.get_yticklabels():
            t1.set_color('r')
    plt.grid()
    if tit:
        plt.title('Comparison average closeness\nNeighbors/Random nodes\nEvolving network',fontsize=28,fontweight='bold')
    plt.tight_layout()
    plt.draw()
    plt.savefig(fileout)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputOverlap',
            type = argparse.FileType('r'),
            help = "File storing overlap, per period, for neigbors and random in the format <period,nbusersTraining,nbusersTesting,neighors,random> (assume header)")
    parser.add_argument('-o','--output',
            type = argparse.FileType('wb'),
            help = "File to save figure")
    parser.add_argument('--title',dest='title',action='store_true')
    parser.add_argument('--notitle',dest='title',action='store_false')
    parser.set_defaults(title=True)
    parser.add_argument('--log',dest='log',action='store_true')
    parser.add_argument('--nolog',dest='log',action='store_false')
    parser.set_defaults(title=False)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    plotSimNUsr(args.inputOverlap,args.output,args.title,args.log)

    args.inputOverlap.close()
    args.output.close()

if __name__ == '__main__':
    main()
