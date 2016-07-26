# -*- coding: utf-8 -*-
import sys,json,re,unicodedata,string
from operator import add
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":   
    def myFunc(s):
        try:
            line = json.loads(s)
        except:
                return []
        if 'twitter' not in line.keys():
            return []
        if 'mention_ids' in  line['twitter']:
            uid = line['twitter']['user']['id']
            return ((uid,1) for h in line['twitter']['mention_ids'])
        else:
            return []
    
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: wordhash <in-file> <out-file>"
        exit(-1)
    #conf = SparkConf.setAppName("PythonWordHash").setMaster()
    sc = SparkContext(appName="PythonUserMentions")
    lines = sc.textFile(sys.argv[1], 1)
    hashwords = lines.flatMap(myFunc) \
                  .map(lambda x: (x[0], x[1])) \
                  .reduceByKey(lambda a,b: a+b)
    hashwords.saveAsTextFile(sys.argv[2])
#    output = counts.take(10)
#    for (word, count) in output:
#        print "%s: %i" % (word, count)

    sc.stop()

