# -*- coding: utf-8 -*-
import sys,json,re,unicodedata,string
from operator import add
from pyspark import SparkContext, SparkConf
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SQLContext 
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import LongType
from pyspark.sql.types import StructType
from pyspark.ml.feature import StringIndexer



if __name__ == "__main__":   
    def myFunc(s):
        try:
            line = json.loads(s)
        except:
            return (('',''))
            #return []
        if 'twitter' not in line.keys():
            return (('',''))
        cont = line['twitter']['text'].strip()
        uid = line['twitter']['user']['id']
        if 'hashtags' in  line['twitter']:
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
        listw = filter(lambda a: a == re.sub('[^a-zA-Z0-9]+','',a),listw)
        listw = filter(lambda a: a != '', listw)
        listw =  ' '.join(listw)
        return ((uid,listw))

    def myFunc2(a,b):
        return a+' '+b
    
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: usertweetidf <in-file> <out-file>"
        exit(-1)
    sc = SparkContext(appName="PythonUserTFIDF")
    lines = sc.textFile(sys.argv[1], 1)
    userwords = lines.map(myFunc).reduceByKey(myFunc2)

    sqlContext = SQLContext(sc)

    # Build schema to build data frame from http://www.nodalpoint.com/spark-data-frames-from-csv-files-handling-headers-column-types/
    fields = [StructField('UserID',LongType(),False),StructField('TweetContent',StringType(),False)]
    schema = StructType(fields)

    #Build data frame
    file_temp = userwords.map(lambda l : (l[0],l[1]))
    df = sqlContext.createDataFrame(file_temp, schema)

###    df.rdd.saveAsTextFile(sys.argv[2]) OK !!

    #Remove empty hashes
#    df_2 = df.filter(df['TweetContent'] != '')
#    df_3 = df_2.filter(df_2['UserID'] != '')

#    df_3.rdd.saveAsTextFile(sys.argv[2])

#    print('Finished removing empty hashes')
#
#    print('After structuring input and filtering, nb records:')
#    file_df_3.count()
#    file_df_3.take(1)
#    
    #Extract TF-IDF From https://spark.apache.org/docs/1.5.2/ml-features.html
    NFeatures=10000
    tokenizer = Tokenizer(inputCol='TweetContent', outputCol='words')
    wordsData = tokenizer.transform(df)
    hashingTF = HashingTF(inputCol='words',outputCol='rawFeatures',numFeatures=NFeatures)
    featurizedData = hashingTF.transform(wordsData)
    idf = IDF(inputCol='rawFeatures',outputCol='features')
    idfModel = idf.fit(featurizedData)
    rescaled_data = idfModel.transform(featurizedData)

    raw_vectors = rescaled_data.drop('words').drop('rawFeatures').drop('TweetContent')

    raw_vectors.rdd.saveAsTextFile(sys.argv[2])

    sc.stop()

