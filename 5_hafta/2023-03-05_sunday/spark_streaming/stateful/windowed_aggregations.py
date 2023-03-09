from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *


spark = SparkSession.builder \
    .appName("windowed_aggregations").getOrCreate()

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

count_by_species = line.groupBy(
    F.window(line.event_time, "1 minutes", "15 seconds"),
    line.Species
).count()



# write to target/sink
checkpointDir = "file:///tmp/streaming/windowed_aggregation"

streamingQuery = (count_by_species.writeStream.format("console")
.outputMode("complete")
                  .trigger(processingTime="4 second")
                  .option("numRows", 20)
                  .option("truncate", False)
                  .option("checkpointLocation", checkpointDir)
                  .start()
 )

streamingQuery.awaitTermination()