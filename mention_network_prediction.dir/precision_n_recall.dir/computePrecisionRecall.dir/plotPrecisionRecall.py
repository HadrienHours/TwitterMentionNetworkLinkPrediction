#*-* encoding::utf-8 *-*
import matplotlib.pyplot as plt
import matplotlib

def plotDifferentStrategies(fileOverlap,fileSimilarity,fileSO,fileSOW1,filesow2):
fileOverlap='best_precision_with_recall_per_period_ONLY_OVERLAP.csv'
fileSimilarity='best_precision_with_recall_per_period_ONLY_SIMILARITY.csv'
fileSO='best_precision_with_recall_per_period_SIMILARITY_N_OVERLAP.csv'
fileSOW1='best_precision_with_recall_per_period_SIMILARITY_N_OVERLAP_0-8_0-2.csv'
fileSOW2='best_precision_with_recall_per_period_SIMILARITY_N_OVERLAP_0-9_0-1.csv'
fileSOW3='best_precision_with_recall_per_period_SIMILARITY_N_OVERLAP_0-2_0-8.csv'
fileSOW4='best_precision_with_recall_per_period_SIMILARITY_N_OVERLAP_0-09_0-91.csv'
fileSOW5='best_precision_with_recall_per_period_SIMILARITY_N_OVERLAP_0-05_0-95.csv'
fo = open(fileOverlap,'r')
fs = open(fileSimilarity,'r')
fso = open(fileSO,'r')
fsow_1 = open(fileSOW1,'r')
fsow_2 = open(fileSOW2,'r')
fsow_3 = open(fileSOW3,'r')
fsow_4 = open(fileSOW4,'r')
fsow_5 = open(fileSOW5,'r')
fo.readline()
fs.readline()
fso.readline()
fsow_1.readline()
fsow_2.readline()
fsow_3.readline()
fsow_4.readline()
fsow_5.readline()
prec_o = [float(line.strip().split(',')[2]) for line in fo]
prec_s = [float(line.strip().split(',')[2]) for line in fs]
prec_so = [float(line.strip().split(',')[2]) for line in fso]
prec_sow_1 = [float(line.strip().split(',')[2]) for line in fsow_1]
prec_sow_2 = [float(line.strip().split(',')[2]) for line in fsow_2]
prec_sow_3 = [float(line.strip().split(',')[2]) for line in fsow_3]
prec_sow_4 = [float(line.strip().split(',')[2]) for line in fsow_4]
prec_sow_5 = [float(line.strip().split(',')[2]) for line in fsow_5]
plt.figure()
plt.plot(range(45),prec_o,'r--',lw=1.5,marker='o',markersize=12,label='Overlap')
plt.plot(range(45),prec_s,'g--',lw=1.5,marker='*',markersize=12,label='Similarity')
plt.plot(range(45),prec_so,'y--',lw=1.5,marker='+',markersize=12,label='SimilarityOverlap')
plt.plot(range(45),prec_sow_1,'m--',lw=1.5,marker='^',markersize=12,label='SimilarityOverlap_0-8_0-2')
plt.plot(range(45),prec_sow_2,'c--',lw=1.5,marker='v',markersize=12,label='SimilarityOverlap_0-9_0-1')
plt.plot(range(45),prec_sow_3,'b--',lw=1.5,marker='x',markersize=12,label='SimilarityOverlap_0-2_0-8')
plt.plot(range(45),prec_sow_4,'k--',lw=1.5,marker='s',markersize=12,label='SimilarityOverlap_0-1_0-9')
plt.plot(range(45),prec_sow_5,'o--',lw=1.5,marker='H',markersize=12,label='SimilarityOverlap_0-05_0-95')
plt.yscale('log')
plt.xlabel('Periods')
plt.ylabel('Precision')
plt.grid()
matplotlib.rcParams.update({'font.size': 22})
plt.legend(fontsize=18)
plt.show(block=False)



fo.seek(0)
fs.seek(0)
fso.seek(0)
fsow_1.seek(0)
fsow_2.seek(0)
fsow_3.seek(0)
fsow_4.seek(0)
fsow_5.seek(0)
fo.readline()
fs.readline()
fso.readline()
fsow_1.readline()
fsow_2.readline()
fsow_3.readline()
fsow_4.readline()
fsow_5.readline()
rec_o = [float(line.strip().split(',')[3]) for line in fo]
rec_s = [float(line.strip().split(',')[3]) for line in fs]
rec_so = [float(line.strip().split(',')[3]) for line in fso]
rec_sow_1 = [float(line.strip().split(',')[3]) for line in fsow_1]
rec_sow_2 = [float(line.strip().split(',')[3]) for line in fsow_2]
rec_sow_3 = [float(line.strip().split(',')[3]) for line in fsow_3]
rec_sow_4 = [float(line.strip().split(',')[3]) for line in fsow_4]
rec_sow_5 = [float(line.strip().split(',')[3]) for line in fsow_5]

plt.figure()
plt.plot(range(45),rec_o,'r--',lw=1.5,marker='o',markersize=12,label='Overlap')
plt.plot(range(45),rec_s,'g--',lw=1.5,marker='*',markersize=12,label='Similarity')
plt.plot(range(45),rec_so,'y--',lw=1.5,marker='+',markersize=12,label='SimilarityOverlap')
plt.plot(range(45),rec_sow_1,'m--',lw=1.5,marker='^',markersize=12,label='SimilarityOverlap_0-8_0-2')
plt.plot(range(45),rec_sow_2,'c--',lw=1.5,marker='v',markersize=12,label='SimilarityOverlap_0-9_0-1')
plt.plot(range(45),rec_sow_3,'b--',lw=1.5,marker='x',markersize=12,label='SimilarityOverlap_0-2_0-8')
plt.plot(range(45),rec_sow_4,'k--',lw=1.5,marker='s',markersize=12,label='SimilarityOverlap_0-1_0-9')
plt.plot(range(45),rec_sow_4,'o--',lw=1.5,marker='H',markersize=12,label='SimilarityOverlap_0-05_0-95')
plt.yscale('log')
plt.xlabel('Periods')
plt.ylabel('Recall')
plt.grid()
matplotlib.rcParams.update({'font.size': 22})
plt.legend(loc='lower left',fontsize=18)
plt.show(block=False)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-io','--inputOverlap',
		type=argparse.FileType('r'),
		required=True,
		help='overlap precsision and recall')
	parser.add_argument('-is','--inputSime',
		type=argparse.FileType('r'),
		required=True,
		help='sim precsision and recall')
	parser.add_argument('-ios','--inputSimilarityOverlap',
		type=argparse.FileType('r'),
		required=True,
		help='overlap+sim precsision and recall')
	parser.add_argument('-iosw1','--inputSimilarityOverlapWeight2',
		type=argparse.FileType('r'),
		required=True,
		help='overlap precsision and recall')
	parser.add_argument('-iosw2','--inputSimilarityOverlapWeight2',
		type=argparse.FileType('r'),
		required=True,
		help='overlap precsision and recall')
	parser.add_argument('-op','--outputprecision',
		type=argparse.FileType('wb'),
		required=True,
		help='name precision figure')
	parser.add_argument('-or','--outputrecall',
		type=argparse.FileType('wb'),
		required=True,
		help='name recall figure')

if __name__ == '__main__':
	main()

