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
            cont = line['twitter']['text'].strip()
            #remove hashtags
            for h in hashtags:
                pattern = re.compile('#'+h,re.IGNORECASE)
                cont = pattern.sub('',cont)
            #remove mentions
            if 'mentions' in line['twitter'].keys():
                for m in line['twitter']['mentions']:
                    pattern = re.compile('@'+m,re.IGNORECASE)
                    cont = pattern.sub('',cont)
            #remove links
            cont = re.sub(r'http[s]*://[^ \t,]+','',cont)
            #remove accent and to lower case
            cont = ''.join(c for c in unicodedata.normalize('NFD', cont) if unicodedata.category(c) != 'Mn').lower()
            #remove punctuation
            cont = cont.replace(',',' ').replace('.',' ').replace('!',' ').replace('?',' ').replace('/',' ')
            exclude = set(string.punctuation)
            cont = ''.join(s for s in cont if s not in exclude)
            listw = re.split('\s+',cont)
            listw = filter(lambda a: a != '', listw)
            listw =  ' '.join(listw)
            hashtags_f = [''.join(c for c in unicodedata.normalize('NFD', h) if unicodedata.category(c) != 'Mn').lower() for h in hashtags]
            if h = ['']:
                return []
            return ((h,listw) for h in hashtags_f)
        else:
            #return (('',''))
            return []
    def myFunc2(a,b):
        return a+' '+b
    
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

