import matplotlib.pyplot as plt
import sys,os,csv,argparse,re,glob
from itertools import cycle
from matplotlib.font_manager import FontProperties


debug=1

def plotSimNUsr(listRatios,listLabels,fileout):
    fontP = FontProperties()
    fontP.set_size('small')
    linespec = ["-","--","-.",":"]
    linecycler = cycle(linespec)

    fig,ax1 = plt.subplots()
#    ax1.set_xlabel('Increasing period',fontsize=20)
#    ax1.set_ylabel('Ratio closeness N/R',fontsize=20)
    for lR,lb in zip(listRatios,listLabels):
        plt.plot(range(len(lR)),lR,next(linecycler),lw=1.5,label=lb)
    plt.legend(loc='upper left',prop=fontP , bbox_to_anchor=(1.0,1.1))
    plt.grid()
#    plt.title('Average closeness ratio \nNeighbor/Random \n per period',fontsize=28,fontweight='bold')
    plt.tight_layout(pad=10)
    plt.draw()
    plt.savefig(fileout)
    plt.close()

def computeRatioList(filesim):
    #remove header
    filesim.readline()
    listsims = list(csv.reader(filesim,delimiter=','))
    listsims1 = []
    for el in listsims:
        listsims1.append([float(el2) for el2 in el[1:]])
    listsim_mention = [el[0] for el in listsims1]
    listsim_random = [el[1] for el in listsims1]
    listratios = [float(i)/float(j) for i,j in zip(listsim_mention,listsim_random)]
    #get legend
    nb = re.findall(r'N_[0-9]',filesim.name)
    rd = re.findall(r'R_[0-9]\-[0-9]',filesim.name)
    if debug > 0:
        print('For file',filesim.name,'Neighbor:',nb[0],'Radius:',rd[0])
    lg = nb[0]+'_'+rd[0]
    return listratios,lg

def main():
    if len(sys.argv) != 3:
        print('Usage ',sys.argv[0],'\tDirfilesims,fileout')
        sys.exit(1)

    if not os.path.isdir(sys.argv[1]):
        print(sys.argv[1],'does not seem to exist')
        sys.exit(1)
    else:
        pathsims = str(sys.argv[1])


    listRatios = []
    listLabels = []
    for filesim in glob.glob(pathsims+'/*.csv'):
        f = open(filesim,'r')
        lr,lb = computeRatioList(f)
        listRatios.append(lr)
        listLabels.append(lb)
        f.close()

    outputFile = sys.argv[-1]

    if os.path.isfile(outputFile):
        print(outputFile,'already exist')
        sys.exit(1)

    outputf = open(outputFile,'wb')
    plotSimNUsr(listRatios,listLabels,outputf)
    outputf.close()


if __name__ == '__main__':
    main()
