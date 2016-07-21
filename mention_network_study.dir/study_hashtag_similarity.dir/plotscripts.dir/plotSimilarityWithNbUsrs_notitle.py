import matplotlib.pyplot as plt
import sys,os,csv,argparse


#Test for externalise legend
from matplotlib.font_manager import FontProperties


def plotSimNUsr(filesim,fileusr,fileout):
    #remove header
    filesim.readline()
    listsims = list(csv.reader(filesim,delimiter=','))
    listsims1 = []
    for el in listsims:
        listsims1.append([float(el2) for el2 in el[1:]])
    listsim_mention = [el[0] for el in listsims1]
    listsim_random = [el[1] for el in listsims1]

    #remove header
    fileusr.readline()
    lu = list(csv.reader(fileusr,delimiter=','))
    listnuser = [int(el[0]) for el in lu]


    fig,ax1 = plt.subplots()
    ax1.bar(range(len(listnuser)),listnuser,alpha=0.4,color='b')
    ax1.set_xlabel('Period',fontsize=24)
    ax1.set_ylabel('Number of users',fontsize=24)
    ax1.yaxis.label.set_color('b')
    for t1 in ax1.get_yticklabels():
            t1.set_color('b')
    ax2 = ax1.twinx()
    ax2.plot(range(len(listsims1)),listsim_mention,'r--',lw=1.5,marker='.',markersize=10,label='Similarity mention neighbors')
    ax2.plot(range(len(listsims1)),listsim_random,'g--',lw=1.5,marker='*',markersize=10,label='Similarity random nodes')
    ax2.set_ylabel('Average Jaccard similarity',fontsize=24)
    ax2.yaxis.label.set_color('r')

    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(prop = fontP)
#    plt.legend(fontsize=12,loc = 'upper right')
    for t1 in ax2.get_yticklabels():
            t1.set_color('r')
    plt.grid()
#    plt.title('Comparison average similarity\nNeighbors/Random nodes',fontsize=28,fontweight='bold')
    plt.tight_layout()
    plt.draw()
    plt.savefig(fileout)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1','--inputSim',
            type = argparse.FileType('r'),
            help = "File storing similarity, per period, for users in the order <neighors,random> (assume header)")
    parser.add_argument('-i2','--inputUsr',
            type = argparse.FileType('r'),
            help = "File storing number of users per period, format: <numberusers,percentage_onecat> (assume header)")
    parser.add_argument('-o','--output',
            type = argparse.FileType('wb'),
            help = "File to save figure")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    plotSimNUsr(args.inputSim,args.inputUsr,args.output)

    args.inputSim.close()
    args.inputUsr.close()
    args.output.close()

if __name__ == '__main__':
    main()
