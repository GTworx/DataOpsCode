from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *


spark = SparkSession.builder \
    .appName("File Source CSV Stateless").getOrCreate()

spark.sparkContext.setLogLevel('ERROR')
df = spark.read.format("csv") \
    .option("header", True) \
    .option("sep", ",") \
    .option("inferSchema", True) \
    .option("timestampFormat", "y-M-d h:m:s.SSSSSS") \
    .load("file:///home/train/data-generator/output2")

stream_schema = df.schema

# read from source
line = spark.readStream.format("csv") \
    .schema(stream_schema) \
    .load("file:///home/train/data-generator/output")

# operation
# SepalLengthCm,SepalWidthCm,PetalLengthCm,PetalWidthCm,Species
# line2 = line.withColumn("SepalLengthCm", F.split(F.col("value"), ",")[0].cast(FloatType())) \
#         .withColumn("SepalWidthCm", F.split(F.col("value"), ",")[1].cast(FloatType())) \
#         .withColumn("PetalLengthCm", F.split(F.col("value"), ",")[2].cast(FloatType())) \
#         .withColumn("PetalWidthCm", F.split(F.col("value"), ",")[3].cast(FloatType())) \
#         .withColumn("Species", F.split(F.col("value"), ",")[4]) \
#         .withColumn("EventTime", F.to_timestamp(F.split(F.col("value"), ",")[5], "y-M-d h:m:s.SSSSSS"))

# line2.printSchema()
line3 = line.filter("Species = 'Iris-versicolor'").drop("value")


# write to target/sink
checkpointDir = "file:///tmp/streaming/file_source_csv2_stateless"

streamingQuery = (line3.writeStream.format("console")
.outputMode("append")
                  .trigger(processingTime="4 second")
                  .option("numRows", 4)
                  .option("truncate", False)
                  .option("checkpointLocation", checkpointDir)
                  .start()
 )

streamingQuery.awaitTermination()