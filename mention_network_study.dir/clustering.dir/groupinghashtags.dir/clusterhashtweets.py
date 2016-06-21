# -*- encoding: utf-8 -*-
import argparse,os,sys,csv
import graphlab

def dbscancluster(filein,fileout,minNeighbors,radius,minTweets):
    sf1 = graphlab.SFrame.read_csv(filein,header=False)
    hashfield = sf1.column_names()[0]
    listwfield = sf1.column_names()[1]
    count1 = sf1.groupby(key_columns=hashfield,operations={'count':graphlab.aggregate.COUNT()})
    sf2 = sf1.unique()
    sf2 = sf2[sf2[listwfield] != '']
    sf2 = sf2.groupby(key_columns=hashfield,operations= {'count':graphlab.aggregate.COUNT(),'text':graphlab.aggregate.CONCAT(listwfield)})
    q99 = sf2['count'].sketch_summary().quantile(0.99)
    sf2 = sf2[(sf2['count'] > minTweets) & (sf2['count'] < q99)]
    sf2['wordcount'] = graphlab.text_analytics.count_words(sf2['text'])
    sf2['tfidf'] = graphlab.text_analytics.tf_idf(sf2['wordcount'])
    dbscan_model = graphlab.dbscan.create(sf2,features=['tfidf'],distance=graphlab.distances.cosine,min_core_neighbors=minNeighbors,radius=radius)
    sf2['clusterid'] = dbscan_model['cluster_id'].sort('row_id')['cluster_id']
    sf2[hashfield,'clusterid'].save(fileout,format='csv')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',
            type=str,
            required=True,
            help="Input csv file: <hash,tweet words>")
    parser.add_argument('-o','--output',
            type=str,
            required=True,
            help="Output csv file: <hash,label> (can be none)")
    parser.add_argument('-n','--minNeighbors',
            type=int,
            default=2,
            help="Minimum number of neighbors for core points in DBSCAN (default 2)")
    parser.add_argument('-r','--radius',
            type=float,
            default=0.7,
            help="Radius of clusters for edge points in DBSCAN (default 0.7)")
    parser.add_argument('-m','--minTweets',
            type=int,
            default=10,
            help="Minimum number of tweets a hashtag has to appear in (default 10)")

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if not os.path.isfile(args.input):
        print(args.input,'does not exist')
        sys.exit(1)

    dbscancluster(args.input,args.output,args.minNeighbors,args.radius,args.minTweets)
    
if __name__ == '__main__':
    main()

