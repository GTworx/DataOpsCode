# rm -r /tmp/streaming/Sensor_Signal/*
# rm -r /home/train/data-generator/output/*
# python dataframe_to_log.py -i ~/datasets/iot_telemetry_data.csv -o ~/data-generator/output

from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder \
    .appName("Sensor Signal Window").getOrCreate()

df = spark.read.format("csv") \
    .option("inferSchema", True) \
    .option("header", True) \
    .load("file:///home/train/data-generator/output_sch")

df1 = df.withColumn("event_time", F.to_timestamp("event_time", "yyyy-MM-dd HH:mm:ss.SSSSSS"))

df1.show(truncate=False)
df1.printSchema()

signal_schema = df1.schema

# read from source
lines = (spark
         .readStream.format("csv")
         .schema(signal_schema)
         .option("header", False)
         .load("file:///home/train/data-generator/output"))

# operation
# count_by_device = lines.groupBy(
#     F.window(lines.event_time, "10 minutes"),
#     lines.device
# ).count()
#
# avg_co = lines.groupBy(
#     F.window(lines.event_time, "10 minutes"),
#     lines.device
# ).avg("co")
#
# avg_humidity = lines.groupBy(
#     F.window(lines.event_time, "10 minutes"),
#     lines.device
# ).avg("humidity")

multiple_agg = lines.groupBy(
    F.window(lines.event_time, "10 minutes"),
    lines.device
).agg(F.count("ts").alias("count"), F.avg("co").alias("avg_co"), F.avg("humidity").alias("avg_humidity"))

checkpointDir = "file:///tmp/streaming/Sensor_Signal"

streamingQuery = (multiple_agg.writeStream.format("console")
                  .outputMode("complete")
                  .trigger(processingTime="4 second")
                  .option("numRows", 20)
                  .option("truncate", False)
                  .option("checkpointLocation", checkpointDir)
                  .start())

streamingQuery.awaitTermination()
