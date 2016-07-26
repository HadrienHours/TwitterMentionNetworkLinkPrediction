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
            return (('noparsing'))
        if 'twitter' not in line.keys():
            return (('notweet'))
        cont = line['twitter']['text'].strip()
        if 'hashtags' in line['twitter'].keys():
            hashtags = line['twitter']['hashtags']
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
        #remove non alphanumeric words
        listw = filter(lambda a: a == re.sub('[^a-zA-Z0-9]+','',a),listw)
        listw = filter(lambda a: a != '', listw)
        listw =  ' '.join(listw)
        if listw == '' or listw == ' ':
            return (('nonnumeric'))
        else:
            return (('tweet'))

    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: wordhash <in-file> <out-file>"
        exit(-1)
    #conf = SparkConf.setAppName("PythonWordHash").setMaster()
    sc = SparkContext(appName="PythonTweetCount")
    lines = sc.textFile(sys.argv[1], 1)
    counts = lines.map(myFunc).map(lambda word: (word,1)).reduceByKey(lambda a,b: a+b)
    #print(counts.take(10))
    #print('******************* YESSSSS ***************************')
    #.map(lambda x: (x[0],x[1]))
    #.reduceByKey(lambda a,b : a+b)
    counts.saveAsTextFile(sys.argv[2])
    sc.stop()

