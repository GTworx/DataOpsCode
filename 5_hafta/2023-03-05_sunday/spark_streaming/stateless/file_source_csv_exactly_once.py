from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *


spark = SparkSession.builder \
    .appName("Exactly Once Recover From Failure").getOrCreate()

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
    .option("maxFilesPerTrigger", 1) \
    .load("file:///home/train/data-generator/output")


# line.printSchema()

# write to target/sink
checkpointDir = "file:///tmp/streaming/file_source_exactly_once"

streamingQuery = (line.writeStream.format("csv")
.outputMode("append")
                  .trigger(processingTime="1 second")
                  .option("header", False)
                  .option("checkpointLocation", checkpointDir)
                  .start("file:///tmp/streaming/exactly_once_out")
 )

streamingQuery.awaitTermination()