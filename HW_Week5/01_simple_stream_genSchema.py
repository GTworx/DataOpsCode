# import findspark
# findspark.init("/opt/manual/spark")
# python dataframe_to_log.py -oh True -i inputIoT/IOT-temp.csv -o /tmp/iot-temp-input-sch

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