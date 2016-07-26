# -*- coding: utf-8 -*-
import sys
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
        print >> sys.stderr, "Usage: ldaClustering <pathToDirInputs> <OutputFile>"
        exit(-1)
        
    
    sc = SparkContext(appName="TF-IDFCorpus")
    sqlContext = SQLContext(sc)
    
    file = sc.textFile(sys.argv[1])
        
    # Build schema to build data frame from http://www.nodalpoint.com/spark-data-frames-from-csv-files-handling-headers-column-types/
    fields = [StructField('Hashname',StringType(),False),StructField('Hashcontent',StringType(),False)]
    schema = StructType(fields)
    
    #Build data frame
    file_temp = file.map(lambda l : l.split(","))
    file_df = sqlContext.createDataFrame(file_temp, schema)
    
    #Extract TF-IDF From https://spark.apache.org/docs/1.5.2/ml-features.html
    tokenizer = Tokenizer(inputCol='Hashcontent', outputCol='words')
    wordsData = tokenizer.transform(file_df)
    hashingTF = HashingTF(inputCol='words',outputCol='rawFeatures',numFeatures=1000)
    featurizedData = hashingTF.transform(wordsData)
    idf = IDF(inputCol='rawFeatures',outputCol='features')
    idfModel = idf.fit(featurizedData)
    rescaled_data = idfModel.transform(featurizedData)
    
    
    # Select subset of columns http://stackoverflow.com/questions/33551407/preparing-data-for-lda-in-spark
    indexer = StringIndexer(inputCol='Hashname',outputCol='HashIndex')
    indexed_data = indexer.fit(rescaled_data).transform(rescaled_data).drop('Hashname').drop('Hashcontent').drop('words').drop('rawFeatures')
    
    #create corpus RDD
    corpus = indexed_data.select("HashIndex", "features").map(list)
    

    corpus.saveAsTextFile(sys.argv[2])

    sqlContext.stop()
    sc.stop()
