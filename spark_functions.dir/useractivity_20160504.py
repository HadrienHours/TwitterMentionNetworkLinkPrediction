# -*- coding: utf-8 -*-
import sys,json,re,unicodedata,string
from operator import add
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":   
    def myFunc(s):
        try:
            line = json.loads(s)
        except:
            return ((''))
        if 'twitter' not in line.keys():
            return ((''))
        else:
            return ((line['twitter']['user']['id']))

    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: wordhash <in-file> <out-file>"
        exit(-1)
    #conf = SparkConf.setAppName("PythonWordHash").setMaster()
    sc = SparkContext(appName="PythonUserCount")
    lines = sc.textFile(sys.argv[1], 1)
    counts = lines.map(myFunc).map(lambda word: (word,1)).reduceByKey(lambda a,b: a+b)
    #print(counts.take(10))
    #print('******************* YESSSSS ***************************')
    #.map(lambda x: (x[0],x[1]))
    #.reduceByKey(lambda a,b : a+b)
    counts.saveAsTextFile(sys.argv[2])
    sc.stop()

