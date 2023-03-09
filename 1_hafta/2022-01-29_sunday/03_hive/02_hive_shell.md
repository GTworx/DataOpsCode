### 1. Connect hive shell
` hive`

### 2. list databases
```
hive> show databases;
OK
default
train
```

### 3. Select a database and list tables in it
```
hive> use train;


hive> show tables;


hote_reviews_orc
hotels_reviews_orc
hotels_reviews_orc_gzip
hotels_reviews_orc_snappy
```

### 4. Sample query
```
hive> select count(*) from hotels_reviews_orc_snappy;
```
- Output
```
Query ID = train_20210130171259_86ec9dde-77d4-4a10-b8ce-30c823455195
Total jobs = 1
Launching Job 1 out of 1
Number of reduce tasks determined at compile time: 1
In order to change the average load for a reducer (in bytes):
  set hive.exec.reducers.bytes.per.reducer=<number>
In order to limit the maximum number of reducers:
  set hive.exec.reducers.max=<number>
In order to set a constant number of reducers:
  set mapreduce.job.reduces=<number>
Starting Job = job_1612007507924_0003, Tracking URL = http://localhost:8088/proxy/application_1612007507924_0003/
Kill Command = /opt/manual/hadoop//bin/mapred job  -kill job_1612007507924_0003
Hadoop job information for Stage-1: number of mappers: 1; number of reducers: 1
2021-01-30 17:13:25,043 Stage-1 map = 0%,  reduce = 0%
2021-01-30 17:13:35,768 Stage-1 map = 100%,  reduce = 0%, Cumulative CPU 6.84 sec
2021-01-30 17:13:47,398 Stage-1 map = 100%,  reduce = 100%, Cumulative CPU 12.75 sec
MapReduce Total cumulative CPU time: 12 seconds 750 msec
Ended Job = job_1612007507924_0003
MapReduce Jobs Launched:
Stage-Stage-1: Map: 1  Reduce: 1   Cumulative CPU: 12.75 sec   HDFS Read: 36323 HDFS Write: 106 SUCCESS
Total MapReduce CPU Time Spent: 12 seconds 750 msec
OK
515738
Time taken: 50.13 seconds, Fetched: 1 row(s)
```
### 5. Exit from hive-shell
`exit;`

