# -*- coding: utf-8 -*-
import sys,json,re,unicodedata,string,datetime,time
from operator import add
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":   
    def myFunc(s):
        try:
            line = json.loads(s)
        except:
            return (('',0.0))
        if 'twitter' not in line.keys():
            return (('',0.0))
        else:
            d = [int(s) for s in re.findall(r'[0-9]+',line['twitter']['created_at'])]
            dt = datetime.datetime(*d[0:6])
            de = time.mktime(time.struct_time(dt.timetuple()))
            uid = line['twitter']['user']['id']
            return ((uid,de))

    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: wordhash <in-file> <out-file>"
        exit(-1)
    #conf = SparkConf.setAppName("PythonWordHash").setMaster()
    sc = SparkContext(appName="PythonUserCount")
    lines = sc.textFile(sys.argv[1], 1)
    counts = lines.map(myFunc).reduceByKey(lambda a,b: min(a,b))
    #print(counts.take(10))
    #print('******************* YESSSSS ***************************')
    #.map(lambda x: (x[0],x[1]))
    #.reduceByKey(lambda a,b : a+b)
    counts.saveAsTextFile(sys.argv[2])
    sc.stop()

