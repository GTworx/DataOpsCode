# Start spark with deltalake support 
` pyspark --master yarn --packages io.delta:delta-core_2.12:1.0.0 `

# Creating your first Delta table
```
>>> data = spark.range(0,5)

>>> data.write.format("delta").save("hdfs://localhost:9000/user/train/delta_intro/data")
```

##Check target location
```
[train@localhost ~]$ hdfs dfs -ls /user/train/delta_intro/data
Found 3 items
drwxr-xr-x   - train supergroup          0 2021-09-28 18:57 /user/train/delta_intro/data/_delta_log
-rw-r--r--   1 train supergroup        471 2021-09-28 18:57 /user/train/delta_intro/data/part-00000-c88d1ad4-0936-495a-8744-605a50f58e7c-c000.snappy.parquet
-rw-r--r--   1 train supergroup        476 2021-09-28 18:57 /user/train/delta_intro/data/part-00001-889222af-1572-422a-828d-e75a6beae599-c000.snappy.parquet
```

## What is in the _delta_log folder
```
[train@localhost ~]$ hdfs dfs -ls /user/train/delta_intro/data/_delta_log/
-rw-r--r--   1 train supergroup        921 2021-09-28 18:57 /user/train/delta_intro/data/_delta_log/00000000000000000000.json
```

## json 
```
[train@localhost ~]$ hdfs dfs -cat /user/train/delta_intro/data/_delta_log/00000000000000000000.json
{"commitInfo":{"timestamp":1632844650979,"operation":"WRITE","operationParameters":{"mode":"ErrorIfExists","partitionBy":"[]"},"isBlindAppend":true,"operationMetrics":{"numFiles":"2","numOutputBytes":"947","numOutputRows":"5"}}}
{"protocol":{"minReaderVersion":1,"minWriterVersion":2}}
{"metaData":{"id":"04224bbc-dbd6-4326-b785-11b0891a204a","format":{"provider":"parquet","options":{}},"schemaString":"{\"type\":\"struct\",\"fields\":[{\"name\":\"id\",\"type\":\"long\",\"nullable\":true,\"metadata\":{}}]}","partitionColumns":[],"configuration":{},"createdTime":1632844633274}}
{"add":{"path":"part-00000-c88d1ad4-0936-495a-8744-605a50f58e7c-c000.snappy.parquet","partitionValues":{},"size":471,"modificationTime":1632844650467,"dataChange":true}}
{"add":{"path":"part-00001-889222af-1572-422a-828d-e75a6beae599-c000.snappy.parquet","partitionValues":{},"size":476,"modificationTime":1632844650627,"dataChange":true}}

```

# Append more data 
```
data2 = spark.range(6,20)
data2.write.format("delta").mode("append").save("hdfs://localhost:9000/user/train/delta_intro/data")
```

## What happened to jsons 
```
hdfs dfs -ls /user/train/delta_intro/data/_delta_log/
Found 2 items
-rw-r--r--   1 train supergroup        921 2021-09-28 18:57 /user/train/delta_intro/data/_delta_log/00000000000000000000.json
-rw-r--r--   1 train supergroup        579 2021-09-28 19:10 /user/train/delta_intro/data/_delta_log/00000000000000000001.json
```

## json1 
```
[train@localhost play]$ hdfs dfs -cat /user/train/delta_intro/data/_delta_log/00000000000000000001.json
{"commitInfo":{"timestamp":1632845424739,"operation":"WRITE","operationParameters":{"mode":"Append","partitionBy":"[]"},"readVersion":0,"isBlindAppend":true,"operationMetrics":{"numFiles":"2","numOutputBytes":"986","numOutputRows":"14"}}}
{"add":{"path":"part-00000-23b444ef-4485-449e-aa8a-22c31d827268-c000.snappy.parquet","partitionValues":{},"size":493,"modificationTime":1632845424703,"dataChange":true}}
{"add":{"path":"part-00001-50d7a319-0505-4964-afa9-f5978988972b-c000.snappy.parquet","partitionValues":{},"size":493,"modificationTime":1632845424275,"dataChange":true}}
```


## Read from delta as spark df
```
spark.read.format("delta").load("/user/train/delta_intro/data").show()
+---+
| id|
+---+
|  9|
| 10|
| 11|
| 12|
| 16|
| 17|
| 18|
| 19|
|  6|
|  7|
|  8|
| 13|
| 14|
| 15|
|  3|
|  4|
|  2|
|  0|
|  1|
+---+

```


# Key difference between parquet and delta 
- The key difference is the `_delta_log` folder which is the Delta transaction log. This
transaction log is key to understanding Delta Lake because it is the underlying infrastructure
for many of its most important features including but not limited to ACID
transactions, scalable metadata handling, and time travel.

# What Is the Delta Lake Transaction Log?
- The Delta Lake transaction log (also known as the Delta Log) is an ordered record of
every change that has ever been performed on a Delta Lake table since its inception.

- To show users correct
views of the data at all times, the Delta Lake transaction log serves as a single
source of truth – the central repository that tracks all changes that users make to the
table.


- See json1 
```
>>> j0.show(truncate=False)
+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------+
|add                                                                                            |commitInfo                                                 |
+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------+
|null                                                                                           |{true, WRITE, {2, 986, 14}, {Append, []}, 0, 1632845424739}|
|{true, 1632845424703, part-00000-23b444ef-4485-449e-aa8a-22c31d827268-c000.snappy.parquet, 493}|null                                                       |
|{true, 1632845424275, part-00001-50d7a319-0505-4964-afa9-f5978988972b-c000.snappy.parquet, 493}|null                                                       |
+-----------------------------------------------------------------------------------------------+-----------------------------------------------------------+



>>> j0 = spark.read.format("json").load("/user/train/delta_intro/data/_delta_log/00000000000000000001.json")


>>> j0.select("commitInfo").where("commitInfo is not null").show(truncate=False)
+-----------------------------------------------------------+
|commitInfo                                                 |
+-----------------------------------------------------------+
|{true, WRITE, {2, 986, 14}, {Append, []}, 0, 1632845424739}|
+-----------------------------------------------------------+

```

## CRC file. 
For each transaction, there is both a JSON file as well as a CRC file. This file
contains key statistics for the table version (i.e. transaction) allowing Delta Lake to
help Spark optimize its queries.
























