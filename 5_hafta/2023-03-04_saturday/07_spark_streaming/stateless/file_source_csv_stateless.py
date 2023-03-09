import findspark

findspark.init("/opt/manual/spark")

from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder \
    .appName("File Source CSV Stateless").getOrCreate()

spark.sparkContext.setLogLevel('ERROR')

df = spark.read.format("csv") \
    .option("inferSchema", True) \
    .option("header", True) \
    .option("timestampFormat", "yyyy-MM-dd hh:mm:ss.SSSSSS") \
    .load("file:///home/train/data-generator/output2")

iris_schema = df.schema

# df.printSchema()
# iris_schema = "ID int, SepalLengthCm float, SepalWidthCm float, PetalLengthCm float, PetalWidthCm float, " \
#               "Species string, event_time timestamp"
#
lines = (spark
         .readStream.format("csv")
         .schema(iris_schema)
         .option("header", False)
         .load("file:///home/train/data-generator/output"))

lines2 = lines.withColumn("my_year", F.year("event_time"))
# grouped_by_species = lines.select( F.explode(F.split(F.col("value"), "\\s+")).alias("word"))
# counts = words.groupBy("word").count()




checkpointDir = "file:///tmp/streaming/file_source_csv_stateless"

streamingQuery = (lines2
                  .writeStream
                  .format("console")
                  .outputMode("append")
                  .trigger(processingTime="1 second")
                  .option("numRows", 4)
                  .option("truncate", False)
                  .option("checkpointLocation", checkpointDir)
                  .start())

# .option("checkpointLocation", checkpointDir)
streamingQuery.awaitTermination()
