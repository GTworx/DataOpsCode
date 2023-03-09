# import findspark

# findspark.init("/opt/manual/spark")

from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder \
    .appName("Simple Stream").getOrCreate()

# spark.sparkContext.setLogLevel('ERROR')

df = spark.read.format("csv") \
    .option("inferSchema", True) \
    .option("header", True) \
    .load("file:///tmp/iot-temp-input-sch")

df1 = df.withColumn("event_time", F.to_timestamp("event_time", "yyyy-MM-dd HH:mm:ss.SSSSSS"))
# .withColumn("noted_date", F.to_timestamp("noted_date", "dd-MM-yyyy HH:mm"))


df1.printSchema()
# iris_schema = "ID int, SepalLengthCm float, SepalWidthCm float, PetalLengthCm float, PetalWidthCm float, " \
#               "Species string, event_time timestamp"
#

# python dataframe_to_log.py -i /home/train/datasets/IOT-temp.csv -o /tmp/iot-temp-input
iot_schema = df1.schema

lines = (spark
         .readStream.format("csv")
         .schema(iot_schema)
         .option("header", False)
         .load("file:///tmp/iot-temp-input"))

lines2 = lines.withColumn("noted_date", F.to_date(F.split(F.col("noted_date"), " ")[0], "dd-MM-yyyy"))
lines3 = lines2.withColumn("noted_year", F.year("noted_date")) \
    .withColumn("noted_month", F.month("noted_date")) \
    .withColumn("noted_day", F.date_format("noted_date", "E"))


def write_to_multiple_sinks(df, batchId):
    df.cache()
    # df.show()

# write to database
    (df.write
     .format("jdbc")
     .mode("append")
     .option("driver", "org.postgresql.Driver")
     .option("url", f"jdbc:postgresql://localhost:5432/traindb")
     .option("dbtable", "spark_streaming")
     .option("user", "train")
     .option("password", "Ankara06")
     .save())

# write to console
    (df.write.format("console")
     .mode("append")
     .option("numRows", 13)
     .option("truncate", False)
     .save())

# write to file
    df.write.format("csv") \
        .mode("append") \
        .option("header", False) \
        .save("file:///tmp/iot-temp-output")

    df.unpersist()


# rm -r /tmp/streaming/Simple_Stream/*
checkpointDir = "file:///tmp/streaming/Simple_Stream"

# streamingQuery = (lines3
#                   .writeStream
#                   .format("console")
#                   .outputMode("append")
#                   .trigger(processingTime="1 second")
#                   .option("numRows", 10)
#                   .option("truncate", False)
#                   .option("checkpointLocation", checkpointDir)
#                   .start())

# streamingQueryCsv = (lines3.writeStream.format("csv")
#                      .outputMode("append")
#                      .trigger(processingTime="1 second")
#                      .option("checkpointLocation", checkpointDir)
#                      .start("file:///tmp/iot-temp-output"))

streamingQuery = (lines3.writeStream
                  .foreachBatch(write_to_multiple_sinks)
                  .trigger(processingTime="1 second")
                  .option("checkpointLocation", checkpointDir)
                  .start()
                  )

streamingQuery.awaitTermination()
