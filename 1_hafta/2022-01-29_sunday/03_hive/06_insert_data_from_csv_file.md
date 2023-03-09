### 1. Notification
Generally we load data to hive from hdfs. However, it is also possible to load from local but not practical. 

### 2. Load data from hdfs

2.1. Create a table that suits data in hdfs.  To learn what to create, better to see data first.
```
[train@localhost ~]$ hdfs dfs -head /user/train/datasets/Advertising.csv
ID,TV,Radio,Newspaper,Sales
1,230.1,37.8,69.2,22.1
2,44.5,39.3,45.1,10.4
3,17.2,45.9,69.3,9.3
4,151.5,41.3,58.5,18.5
..
..
```
#### 2.2. Create table. 
There is header line in the data. We have to specify during the create statement as table properties.
```
[train@localhost ~]$ beeline -u jdbc:hive2://localhost:10000

# close warnings
jdbc:hive2://localhost:10000> set hive.server2.logging.operation.level=NONE;

# select test1 database
use test1;

# Drop table 
drop table test1.advertising;

# create table again
create table if not exists test1.advertising
(id int, tv float, radio float, newspaper float, sales float)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
tblproperties('skip.header.line.count'='1');


# inspect table
 describe test1.advertising;
+------------+------------+----------+
|  col_name  | data_type  | comment  |
+------------+------------+----------+
| id         | int        |          |
| tv         | float      |          |
| radio      | float      |          |
| newspaper  | float      |          |
| sales      | float      |          |
+------------+------------+----------+


# Is there any record?
 select * from test1.advertising;
+-----------------+-----------------+--------------------+------------------------+--------------------+
| advertising.id  | advertising.tv  | advertising.radio  | advertising.newspaper  | advertising.sales  |
+-----------------+-----------------+--------------------+------------------------+--------------------+
+-----------------+-----------------+--------------------+------------------------+--------------------+
```

#### 2.3. Load data to hive table
```
load data inpath '/user/train/datasets/Advertising.csv' into table test1.advertising;

```
#### 2.4. See the data
```
 select * from test1.advertising limit 3;
+-----------------+-----------------+--------------------+------------------------+--------------------+
| advertising.id  | advertising.tv  | advertising.radio  | advertising.newspaper  | advertising.sales  |
+-----------------+-----------------+--------------------+------------------------+--------------------+
| 1               | 230.1           | 37.8               | 69.2                   | 22.1               |
| 2               | 44.5            | 39.3               | 45.1                   | 10.4               |
| 3               | 17.2            | 45.9               | 69.3                   | 9.3                |
+-----------------+-----------------+--------------------+------------------------+--------------------+
```

#### 2.5. Check data in hdfs  
`  [train@localhost ~]$ hdfs dfs -ls /user/train/datasets | grep Advertising  `   
You will see the data has gone where is it now?  
It is in the default hive warehouse directory. Let's check it.
```
[train@localhost ~]$ hdfs dfs -ls /user/hive/warehouse/test1.db/advertising
Found 1 items
-rw-r--r--   1 train supergroup       4556 2020-09-16 14:58 /user/hive/warehouse/test1.db/advertising/Advertising.csv
```

#### 2.6. If you see the result like this
```
 select * from test1.advertising limit 10;
+-----------------+-----------------+--------------------+------------------------+--------------------+
| advertising.id  | advertising.tv  | advertising.radio  | advertising.newspaper  | advertising.sales  |
+-----------------+-----------------+--------------------+------------------------+--------------------+
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
+-----------------+-----------------+--------------------+------------------------+--------------------+
```
It is possibly due to schema data conflict. Check your create table and properties.
If you try second time, don't forget to -put your data to hdfs again because it has already gone.


#### 2.7. load overwrite mode  
put data to hdfs 
`  [train@localhost big_data]$ hdfs dfs -put ~/datasets/Advertising.csv /user/train/datasets  `

#### 2.9. Load again  

```
# Check record count
select count(1) from test1.advertising;
+------+
| _c0  |
+------+
| 200  |
+------+


# load the same data overwrite
 load data inpath '/user/train/datasets/Advertising.csv' overwrite into table test1.advertising;


select count(1) from advertising;
+------+
| _c0  |
+------+
| 200  |
+------+
1 row selected (38.973 seconds)

```
See there is still 200 records.

#### 2.10. Load with append
-  put data hdfs again
` [train@localhost big_data]$ hdfs dfs -put ~/datasets/Advertising.csv /user/train/datasets  `

```
load data inpath '/user/train/datasets/Advertising.csv' into table test1.advertising;


# count
select count(1) from advertising;
+------+
| _c0  |
+------+
| 400  |
+------+
```

**into appends, overwrite into overwrites.**  

### 3. Load data from local
```
load data local inpath '/home/train/datasets/Advertising.csv' into table test1.advertising;

# count
select count(1) from advertising;
+------+
| _c0  |
+------+
| 600  |
+------+
```

### Load averwrite data again last time.