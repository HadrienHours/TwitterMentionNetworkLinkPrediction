# -*- coding: utf-8 -*-
import sys,json,re,unicodedata,string
from operator import add
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":   
    def myFunc(s):
        try:
            line = json.loads(s)
        except:
                # return (('',''))
                return []
        if 'twitter' not in line.keys():
            return(('',''))
        if 'hashtags' in  line['twitter']:
            hashtags = line['twitter']['hashtags']
            hashtags_f = [''.join(c for c in unicodedata.normalize('NFD', h) if unicodedata.category(c) != 'Mn').lower() for h in hashtags]
            hashtags_f = [h for h in hashtags_f if h == re.sub('[^a-zA-Z0-9]+','',h)]
            if hashtags_f == ['']:
                return []
            return ((h,1) for h in hashtags_f)
        else:
            #return (('',''))
            return []
    def myFunc2(a,b):
        return a+b
    
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: wordhash <in-file> <out-file>"
        exit(-1)
    #conf = SparkConf.setAppName("PythonWordHash").setMaster()
    sc = SparkContext(appName="PythonWordHash")
    lines = sc.textFile(sys.argv[1], 1)
    hashwords = lines.flatMap(myFunc) \
                  .map(lambda x: (x[0], x[1])) \
                  .reduceByKey(myFunc2)
    hashwords.saveAsTextFile(sys.argv[2])
#    output = counts.take(10)
#    for (word, count) in output:
#        print "%s: %i" % (word, count)

    sc.stop()

