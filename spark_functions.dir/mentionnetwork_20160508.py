# -*- coding: utf-8 -*-
import sys,json,re,unicodedata,string
from operator import add
from pyspark import SparkContext, SparkConf
import datetime,time

if __name__ == "__main__":   
    def myFunc(s):
        try:
            line = json.loads(s)
        except:
                return (((0,0),(0,0)))
        if 'twitter' not in line.keys():
            return (((0,0),(0,0)))
        if 'mention_ids' in  line['twitter']:
            uid = line['twitter']['user']['id']
            dt1 = [int(i) for i in re.findall(r'[0-9]+',line['twitter']['created_at'])]
            dt2 = datetime.datetime(*dt1[0:6])
            dt3 = time.mktime(time.struct_time(dt2.timetuple()))
            lm = []
            for mid_t in line['twitter']['mention_ids']:
                mid = int(mid_t)
                if mid < uid:
                    lm.append([mid,uid,(0,dt3),(0,1)])
                else:
                    lm.append([uid,mid,(dt3,0),(1,0)])
            return (((m[0],m[1]),(m[2],m[3])) for m in lm)
        else:
            return []
   
    def myFunc2(x1,x2):
        print('Input1',x1)
        print('Input2',x2)
        return (min(x1[0][0],x2[0][0]),max(x1[0][0],x2[0][0]),min(x1[0][1],x2[0][1]),max(x1[0][1],x2[0][1]),x1[1][0]+x2[1][0],x1[1][1]+x2[1][1])

    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: mentionnetwork  <in-file> <out-file>"
        exit(-1)
    #conf = SparkConf.setAppName("PythonWordHash").setMaster()
    sc = SparkContext(appName="PythonNetworkMentions")
    lines = sc.textFile(sys.argv[1], 1)
    hashwords = lines.flatMap(myFunc) \
#                  .reduceByKey(myFunc2)
#                  .map(lambda x: (tuple(x[0]), x[1]))
    hashwords.saveAsTextFile(sys.argv[2])
#                  .map(lambda x: (tuple(x[0]), x[1])) \

#    output = counts.take(10)
#    for (word, count) in output:
#        print "%s: %i" % (word, count)

    sc.stop()

