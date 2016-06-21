import matplotlib.pyplot as plt
import sys,os,csv,argparse


def plotSimNUsr(fileoverlap,fileout,tit,log):
    #remove header
    fileoverlap.readline()
    listoverlaps = list(csv.reader(fileoverlap,delimiter=','))
    listoverlaps1 = []
    for el in listoverlaps:
        listoverlaps1.append([float(el2) for el2 in el[1:]])
    listnuser = [int(el[0]) for el in listoverlaps1]
    listoverlap_mention = [el[1] for el in listoverlaps1]
    listoverlap_random = [el[2] for el in listoverlaps1]

    fig,ax1 = plt.subplots()
    ax1.bar(range(len(listnuser)),listnuser,alpha=0.4,color='b')
    ax1.set_xlabel('Increasing period',fontsize=24)
    ax1.set_ylabel('Number of mentions',fontsize=24)
    ax1.yaxis.label.set_color('b')
    for t1 in ax1.get_yticklabels():
            t1.set_color('b')
    ax2 = ax1.twinx()
    ax2.plot(range(len(listoverlaps1)),listoverlap_mention,'r--',lw=1.5,marker='.',markersize=10,label='Overlap mention neighbors')
    ax2.plot(range(len(listoverlaps1)),listoverlap_random,'g--',lw=1.5,marker='*',markersize=10,label='Overlap random nodes')
    ax2.set_ylabel('Average overlap for users',fontsize=24)
    if log:
        ax2.set_yscale('log')
    ax2.yaxis.label.set_color('r')
    plt.legend(fontsize=12,loc = 'lower right')
    for t1 in ax2.get_yticklabels():
            t1.set_color('r')
    plt.grid()
    if tit:
        plt.title('Comparison average overlap\nNeighbors/Random nodes\nEvolving network',fontsize=28,fontweight='bold')
    plt.tight_layout()
    plt.draw()
    plt.savefig(fileout)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputOverlap',
            type = argparse.FileType('r'),
            help = "File storing overlap, per period, for neigbors and random in the format <period,nbusers,neighors,random> (assume header)")
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
