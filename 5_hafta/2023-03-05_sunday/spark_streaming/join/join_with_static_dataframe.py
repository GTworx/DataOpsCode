from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *


spark = SparkSession.builder \
    .appName("Join").getOrCreate()

spark.sparkContext.setLogLevel('ERROR')
df = spark.read.format("csv") \
    .option("header", True) \
    .option("sep", ",") \
    .option("inferSchema", True) \
    .option("timestampFormat", "y-M-d h:m:s.SSSSSS") \
    .load("file:///home/train/data-generator/output2")

stream_schema = df.schema

# read static df (products)
df_products = spark.read.format("csv") \
    .option("header", True) \
    .option("sep", ",") \
    .option("inferSchema", True) \
    .load("file:///home/train/datasets/retail_db/products.csv").cache()

# read from source
line = spark.readStream.format("csv") \
    .schema(stream_schema) \
    .load("file:///home/train/data-generator/output")

line.printSchema()

line2 = line.join(df_products, line.orderItemProductId == df_products.productId) \
    .select("orderItemName","orderItemOrderId","orderItemProductId","orderItemQuantity","orderItemSubTotal"
            ,"orderItemProductPrice", "productId", "productName")

# write to target/sink
checkpointDir = "file:///tmp/streaming/streaming_join"

# streamingQuery = (line2.writeStream.format("console")
# .outputMode("append")
#                   .trigger(processingTime="4 second")
#                   .option("numRows", 4)
#                   .option("truncate", False)
#                   .option("checkpointLocation", checkpointDir)
#                   .start()
#  )

streamingQuery = (line2.writeStream.format("console")
.outputMode("append")
                  .trigger(processingTime="4 second")
                  .option("numRows", 4)
                  .option("truncate", False)
                  .option("checkpointLocation", checkpointDir)
                  .start()
 )


streamingQuery.awaitTermination()