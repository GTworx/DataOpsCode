
-- write these tables with spark
/**
[train@localhost ~]$ wget -P ~/datasets https://github.com/erkansirin78/datasets/raw/master/Hotel_Reviews.csv.gz

[train@localhost ~]$ hdfs dfs -put ~/datasets/Hotel_Reviews.csv.gz /user/train/datasets

[train@localhost ~]$ pyspark --master yarn

>>> df = spark.read.format("csv") \
.option("header",True) \
.option("compression","gzip") \
.option("inferSchema",True) \
.load("/user/train/datasets/Hotel_Reviews.csv.gz")


>>> df.write.format("parquet").mode("overwrite").saveAsTable("test1.hotels_parquet")
 
>>> spark.sql("select count(1) from test1.hotels_parquet").show()
+--------+
|count(1)|
+--------+
|  515738|
+--------+

>>> exit()

*/
-- select db
use test1;

-- check
select count(1) from test1.hotels_parquet;
+---------+
|   _c0   |
+---------+
| 515738  |
+---------+
1 row selected (43.881 seconds)


select hotel_name, average_score,review_date from test1.hotels_parquet limit 5;
/*
hotel_name |average_score|review_date|
-----------+-------------+-----------+
Hotel Arena|          7.7|8/3/2017   |
Hotel Arena|          7.7|8/3/2017   |
Hotel Arena|          7.7|7/31/2017  |
Hotel Arena|          7.7|7/31/2017  |
Hotel Arena|          7.7|7/24/2017  |          |
 */


describe formatted test1.hotels_parquet;

/*
-- To increase performance and reduce traffic between nodes and mappers it is better to compress intermediate results.
SET hive.intermediate.compression.codec=org.apache.hadoop.io.compress.SnappyCodec;
*/

/*
-- Set properties for snappy compression 
-- When the hive.exec.compress.output property is set to true, Hive will
use the codec configured by the mapreduce.output.fileoutputformat.compress.codec property to compress the
data in HDFS as follows. These properties can be set in the hive-site.xml or in the
command-line session:

SET hive.exec.compress.output=true;
SET mapreduce.output.fileoutputformat.compress.codec=org.apache.hadoop.io.compress.SnappyCodec;

SET mapred.output.compression.codec=org.apache.hadoop.io.compress.SnappyCodec;
SET mapred.output.compression.type=BLOCK;
*/

-- orc
create table test1.hotels_orc stored as orc TBLPROPERTIES ('orc.compress'='NONE') 
as select * from test1.hotels_parquet ;
-- 47.782 seconds

-- parquet
create table test1.hotels_parquet2 stored as parquet TBLPROPERTIES ('parquet.compression'='UNCOMPRESSED') 
as select * from test1.hotels_parquet ;
-- 45.48 seconds

--textfile
create table test1.hotels_text stored as textfile 
as select * from test1.hotels_parquet;
-- 39.779 seconds





-- with compression 

-- orc_snappy orc.compress = {NONE, ZLIB, SNAPPY} default ZLIB
create table test1.hotels_orc_snappy stored as orc TBLPROPERTIES ('orc.compress'='SNAPPY') 
as select * from test1.hotels_parquet;
-- 48.436 seconds

-- orc_zlib
create table test1.hotels_orc_zlib stored as ORC TBLPROPERTIES ('orc.compress'='ZLIB') 
as select * from test1.hotels_parquet;
-- 42.781 seconds


-- parquet_snappy
create table test1.hotels_parquet_snappy stored as parquet TBLPROPERTIES ('parquet.compression'='SNAPPY') 
as select * from test1.hotels_parquet;
-- 41.447 seconds


-- parquet_gzib
create table test1.hotels_parquet_gzib stored as parquet TBLPROPERTIES ('parquet.compression'='GZIP') 
as select * from test1.hotels_parquet;
-- 58.176 seconds


-- text_snappy
SET hive.exec.compress.output=true;
SET io.textfile.compression.type=SNAPPY;

create table test1.hotels_text_snappy stored as textfile 
as select * from test1.hotels_parquet;
-- 46.127 seconds

-- see the disk usage
/*
[train@localhost ~]$ hdfs dfs -du -h /user/hive/warehouse/test1.db
[size]   [disk space consumed]
112.7 M  338.0 M  /user/hive/warehouse/test1.db/hotels_orc
55.4 M   166.3 M  /user/hive/warehouse/test1.db/hotels_orc_snappy
40.4 M   121.1 M  /user/hive/warehouse/test1.db/hotels_orc_zlib

60.2 M   60.2 M   /user/hive/warehouse/test1.db/hotels_parquet  (spark write original)
148.4 M  445.3 M  /user/hive/warehouse/test1.db/hotels_parquet2
36.5 M   109.6 M  /user/hive/warehouse/test1.db/hotels_parquet_gzib
62.7 M   188.0 M  /user/hive/warehouse/test1.db/hotels_parquet_snappy

226.0 M  677.9 M  /user/hive/warehouse/test1.db/hotels_text
44.2 M   132.7 M  /user/hive/warehouse/test1.db/hotels_text_snappy

 */
-- https://community.cloudera.com/t5/Support-Questions/Explain-hdfs-du-command-output/td-p/46586

show tables;
drop table hotels_text_snappy;


-- https://blog.yannickjaquier.com/hadoop/orc-versus-parquet-compression-and-response-time.html
-- 









