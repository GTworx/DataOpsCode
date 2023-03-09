# rm -r /tmp/streaming/Sensor_Signal/*
# rm -r /home/train/data-generator/output/*
# python dataframe_to_log.py -oh True -i /home/train/datasets/iot_telemetry_data.csv -o ~/data-generator/output

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