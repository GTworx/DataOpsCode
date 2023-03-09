### 1. Select test1 database
`use test1;`

### 2. Create simple table with default properties
```
create table if not exists test1.mytable(id int, user_name string, email array<string>);
No rows affected (0.25 seconds)

show tables;
+-----------+
| tab_name  |
+-----------+
| mytable   |
+-----------+
1 row selected (0.097 seconds)
```

### 3. Describe table
```
describe test1.mytable;
+------------+----------------+----------+
|  col_name  |   data_type    | comment  |
+------------+----------------+----------+
| id         | int            |          |
| user_name  | string         |          |
| email      | array<string>  |          |
+------------+----------------+----------+
3 rows selected (0.113 seconds)
```

### 4. More information for table
```
describe formatted  test1.mytable;
```
### 5. drop table 
` drop table test1.mytable;`

### 6. Create table with properties
```
0: jdbc:hive2://localhost:10000> create table if not exists test1.mytable (id int, username string, email array<string>)
. . . . . . . . . . . . . . . .> row format delimited
. . . . . . . . . . . . . . . .> fields terminated by ','
. . . . . . . . . . . . . . . .> collection items terminated by ':'
. . . . . . . . . . . . . . . .> lines terminated by '\n'
. . . . . . . . . . . . . . . .> stored as textfile;
```
- copy paste ready version
```
create table if not exists test1.mytable 
(id int, username string, email array<string>)
row format delimited
fields terminated by ','
collection items terminated by ':'
lines terminated by '\n'
stored as textfile;
```

### 7. generate create script from existing table
```
show create table test1.mytable;

+----------------------------------------------------+
|                   createtab_stmt                   |
+----------------------------------------------------+
| CREATE TABLE `mytable`(                            |
|   `id` int,                                        |
|   `username` string,                               |
|   `email` array<string>)                           |
| ROW FORMAT SERDE                                   |
|   'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'  |
| WITH SERDEPROPERTIES (                             |
|   'collection.delim'=':',                          |
|   'field.delim'=',',                               |
|   'line.delim'='\n',                               |
|   'serialization.format'=',')                      |
| STORED AS INPUTFORMAT                              |
|   'org.apache.hadoop.mapred.TextInputFormat'       |
| OUTPUTFORMAT                                       |
|   'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' |
| LOCATION                                           |
|   'hdfs://localhost:9000/user/hive/warehouse/test1.db/mytable' |
| TBLPROPERTIES (                                    |
|   'bucketing_version'='2',                         |
|   'transient_lastDdlTime'='1600272299')            |
+----------------------------------------------------+
20 rows selected (0.264 seconds)
```

## 8. Show tblproperties
```
0: jdbc:hive2://localhost:10000> show tblproperties test1.mytable;
+------------------------+----------------------------------------------------+
|       prpt_name        |                     prpt_value                     |
+------------------------+----------------------------------------------------+
| COLUMN_STATS_ACCURATE  | {"BASIC_STATS":"true","COLUMN_STATS":{"email":"true","id":"true","user_name":"true"}} |
| bucketing_version      | 2                                                  |
| numFiles               | 0                                                  |
| numRows                | 0                                                  |
| rawDataSize            | 0                                                  |
| totalSize              | 0                                                  |
| transient_lastDdlTime  | 1620984954                                         |
+------------------------+----------------------------------------------------+
7 rows selected (0.11 seconds)
```