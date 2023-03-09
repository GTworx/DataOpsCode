### 1. Check if hive metastore is running  
```
[train@localhost play]$ pgrep -f org.apache.hive.service.server.HiveServer2
226646
```
If you can't see pid. Probably Hadoop-Yarn-Hive is not running or hive has not completely started yet. 
Run with `start-all.sh`  

### 2. Check if hiveserver2 is running  
```
[train@localhost play]$ pgrep -f org.apache.hadoop.hive.metastore.HiveMetaStore
226957
```
### 3. Beeline connection  
`[train@localhost play]$ beeline -u jdbc:hive2://127.0.0.1:10000`

You should see `0: jdbc:hive2://127.0.0.1:10000>` means beeline shell is ready to use.  
Close logs  
`  0: jdbc:hive2://127.0.0.1:10000> set hive.server2.logging.operation.level=NONE;  `  

### 4. List databases
```
0: jdbc:hive2://localhost:10000> show databases;


+----------------+
| database_name  |
+----------------+
| default        |
| train          |
+----------------+
```

### 5. Select a database and list tables
```
0: jdbc:hive2://localhost:10000> use bookstore;


0: jdbc:hive2://localhost:10000> show tables;

+----------------------------+
|          tab_name          |
+----------------------------+
| hote_reviews_orc           |
| hotels_reviews_orc         |
| hotels_reviews_orc_gzip    |
| hotels_reviews_orc_snappy  |
+----------------------------+

```

###  6. exit from beeline
` !q `