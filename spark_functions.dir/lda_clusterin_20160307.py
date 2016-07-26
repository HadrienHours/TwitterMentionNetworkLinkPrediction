# -*- coding: utf-8 -*-
import sys,re,codecs,time
from pyspark import SparkContext, SparkConf
from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SQLContext 
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType
from pyspark.sql.types import StructType
from pyspark.ml.feature import StringIndexer


if __name__ == "__main__":
      
    if (len(sys.argv) != 3) or (len(sys.argv) > 5):
        print >> sys.stderr, "Usage: ldaClustering <pathToDirInputs> <OutputFile> <K(opt)><maxIT(opt)>"
        exit(-1)
        
    
    sc = SparkContext(appName="LDA Clustering")
    sqlContext = SQLContext(sc)
    
    file = sc.textFile(sys.argv[1])


    #reformat the crawler output
    def reformatLine(l):
        l1 = l.strip("(").strip(")")
        l2 = l1.replace('u\'','')
        l3 = l2.replace('\'','')
        l4 = codecs.unicode_escape_decode(l3)[0]
        return l4

    filef = file.map(reformatLine)
        
    # Build schema to build data frame from http://www.nodalpoint.com/spark-data-frames-from-csv-files-handling-headers-column-types/
    fields = [StructField('Hashname',StringType(),False),StructField('Hashcontent',StringType(),False)]
    schema = StructType(fields)
    
    #Build data frame
    file_temp = filef.map(lambda l : l.split(","))
    file_df = sqlContext.createDataFrame(file_temp, schema)
   
    print("Data Frame built")

    filef.unpersist()
    file_temp.unpersist()
    print("Deleted input files to create dataframe")


    #Remove empty hashes
    file_df = file_df.filter(file_df['Hashname'] != '')

    #Extract TF-IDF From https://spark.apache.org/docs/1.5.2/ml-features.html
    NFeatures=10000
    tokenizer = Tokenizer(inputCol='Hashcontent', outputCol='words')
    wordsData = tokenizer.transform(file_df)
    hashingTF = HashingTF(inputCol='words',outputCol='rawFeatures',numFeatures=NFeatures)
    featurizedData = hashingTF.transform(wordsData)
    idf = IDF(inputCol='rawFeatures',outputCol='features')
    idfModel = idf.fit(featurizedData)
    rescaled_data = idfModel.transform(featurizedData)
    
    print("Tokenized words")

    #Remove useless fields
    raw_vectors = rescaled_data.drop('words').drop('rawFeatures').drop('Hashcontent')
    rescaled_data.unpersist()

    # Select subset of columns http://stackoverflow.com/questions/33551407/preparing-data-for-lda-in-spark
    indexer = StringIndexer(inputCol='Hashname',outputCol='HashIndex')
    indexer_f = indexer.fit(raw_vectors)
    indexed_data = indexer_f.transform(raw_vectors)
    print("Indexed rows with hashtag")

    inputd = indexed_data.select(indexed_data.HashIndex.cast("long").alias("Index"), indexed_data.features)
    
    c = inputd.count()
    l = inputd.take(1)
    
    print("Sucessful cast of index to integer")
    print("Number of records",c)
    print("First record:")
    print(l)

    #create corpus RDD
    corpus = inputd.map(list)
    
    #LDA clustering
    if len(sys.argv) == 3:
        K = 3
        maxIT = 100
    elif len(sys.argv) == 4:
        K = sys.argv[3]
        maxIT = 100
    else:
        K = sys.argv[3]
        maxIT = sys.argv[4]
    
    print("Start training LDA model with ",K," clusters ",maxIT," maximum iteration")
    modelLDA = LDA.train(corpus,k=K,maxIterations=maxIT)
    print("Model trained successfully")
    
    #Save model
    modelLDA.save(sc, sys.argv[2])
    print("Model saved successfully")

    #Test
    time.sleep(300)

    sc.stop()
