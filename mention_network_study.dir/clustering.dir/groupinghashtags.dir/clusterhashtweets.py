# -*- encoding: utf-8 -*-
import argparse,os,sys,csv,pandas as pn
import graphlab

def dbscancluster(filein,fileout,minNeighbors,radius,minTweets):

    #use panda data frame to read compressed file and cast string format
    df1 = pn.read_csv(filein,compression='gzip',dtype={'hashtag':str,'text':str},header=-1)
    df1[0] = df1[0].apply(lambda x: str(x))
    df1[1] = df1[1].apply(lambda x: str(x))

    #Load the resulting data in Graphlab SFrame
    sf1 = graphlab.SFrame(data=df1)
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
    df2 = sf2[hashfield,'clusterid'].to_dataframe()
    print('About to launch following cmd')
    print('df2.to_csv('+fileout+',compression=\'gzip\',header=False)')
    df2.to_csv(fileout,compression='gzip',header=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',
            type=argparse.FileType('r'),
            default=sys.stdin,
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
            default=0.5,
            help="Radius of clusters for edge points in DBSCAN (default 0.7)")
    parser.add_argument('-m','--minTweets',
            type=int,
            default=10,
            help="Minimum number of tweets a hashtag has to appear in (default 10)")

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    dbscancluster(args.input,args.output,args.minNeighbors,args.radius,args.minTweets)
    
if __name__ == '__main__':
    main()

