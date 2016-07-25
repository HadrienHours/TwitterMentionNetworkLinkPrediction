import matplotlib.pyplot as plt
import sys,os,csv,argparse


def plotSimNUsr(filehashsim,fileout,tit,log):

#    plt.figure(figsize=(6, 8))


    #define the axes positions
    left = bottom = 0.1
    width = height = 0.7

    #remove header
    filehashsim.readline()
    hashsims = list(csv.reader(filehashsim,delimiter=','))
    hashsim1 = []
    for el in hashsims:
        hashsim1.append([float(el2) for el2 in el[1:]])
    listNTweetsTraining = [int(el[0]) for el in hashsim1]
    listNTweetsTesting = [int(el[1]) for el in hashsim1]
    listNTraining = [int(el[2]) for el in hashsim1 ]
    listNTesting = [int(el[3]) for el in hashsim1]
    hasim_neighbor = [el[4] for el in hashsim1]
    hasim_random = [el[5] for el in hashsim1]

    plt.figure()
    ax_main = plt.axes([left,bottom,width,height])
    ax_top = plt.axes([left,bottom+height+0.03,width,0.15])
    ax_main.bar(range(len(listNTraining)),listNTraining,alpha=0.4,color='b')
    #ax_main.set_xlabel('Increasing period',fontsize=24)
    ax_main.set_ylabel('Number of mentions',fontsize=24)
    #if log:
    ax_main.set_yscale('log')
    ax_main.yaxis.label.set_color('b')
    for t1 in ax_main.get_yticklabels():
            t1.set_color('b')
    #ax2 = ax1.twinx()
    ax_main.bar(range(len(listNTesting)),listNTesting,alpha=0.6,color='b')

    ax3 = ax_main.twinx()
    ax3.plot(range(len(hashsim1)),hasim_neighbor,'r--',lw=1.5,marker='*',markersize=10,label='Hashtag similarity neighbors')
    ax3.plot(range(len(hashsim1)),hasim_random,'r--',lw=1.5,marker='.',markersize=12,label='Hashtag similarity average')
    ax3.set_ylabel('Average hashtag similarity for users',fontsize=24)
    if log:
        ax3.set_yscale('log')
    ax3.yaxis.label.set_color('r')
    plt.legend(fontsize=12,loc = 'center left')
    for t1 in ax3.get_yticklabels():
            t1.set_color('r')
    plt.grid()

    ax_top.bar(range(len(listNTweetsTraining)),listNTweetsTraining,alpha=0.4,color='g')
    ax_top.bar(range(len(listNTweetsTesting)),listNTweetsTesting,alpha=0.6,color='g')

    ax_top.set_yscale('log')
    ax_top.set_xticklabels([])


    if tit:
        plt.title('Comparison average hash similarity\nNeighbors/Random nodes\nEvolving network',fontsize=28,fontweight='bold')
    #plt.tight_layout()
    plt.draw()
    plt.savefig(fileout)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Plot hashtag similarity neighbor vs average with number of mentions and number of tweets for the diffrent testing/training periiods")
    parser.add_argument('-i','--inputHashsim',
            type = argparse.FileType('r'),
            help = "File storing overlap, per period, for neigbors and random in the format <period,nbTweetsTraining,nbTweetsTesting,nbMentionsTraining,nbMentionsTraining,hashsimneighors,hashsimrandom> (assume header)")
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

    plotSimNUsr(args.inputHashsim,args.output,args.title,args.log)

    args.inputHashsim.close()
    args.output.close()

if __name__ == '__main__':
    main()
