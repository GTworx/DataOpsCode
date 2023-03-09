from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *

spark = SparkSession.builder.appName("For Each Batch") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1") \
    .getOrCreate()

line = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092,localhost:9292") \
    .option("subscribe", "topic1") \
    .load()

# deserialize
line2 = line.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "topic", "partition")

# Parsing
# SepalLengthCm,SepalWidthCm,PetalLengthCm,PetalWidthCm,Species
line3 = line2.withColumn("SepalLengthCm", F.split(F.col("value"), ",")[0].cast(FloatType())) \
    .withColumn("SepalWidthCm", F.split(F.col("value"), ",")[1].cast(FloatType())) \
    .withColumn("PetalLengthCm", F.split(F.col("value"), ",")[2].cast(FloatType())) \
    .withColumn("PetalWidthCm", F.split(F.col("value"), ",")[3].cast(FloatType())) \
    .withColumn("Species", F.split(F.col("value"), ",")[4]) \
    .drop("value")

# operation
line4 = line3.withColumn("sum_sepal", (line3.SepalLengthCm + line3.SepalWidthCm)) \
    .withColumn("sum_petal", (line3.PetalLengthCm + line3.PetalWidthCm))


def write_to_multiple_sinks(df, batchId):
    df.cache()
    df.show()

    (df.write
     .format("jdbc")
     .mode("append")
     .option("driver", "org.postgresql.Driver")
     .option("url", f"jdbc:postgresql://localhost:5432/traindb")
     .option("dbtable", "spark_streaming")
     .option("user", "train")
     .option("password", "Ankara06")
     .save())

    df.write.format("csv") \
        .mode("append") \
        .save("file:///tmp/streaming/for_each_batch_output")

    df.unpersist()


checkpointDir = "file:///tmp/streaming/for_each_batch_kafka"

streamingQuery = (line4.writeStream
                  .foreachBatch(write_to_multiple_sinks)
                  .option("checkpointLocation", checkpointDir)
                  .start()
                  )

streamingQuery.awaitTermination()
