-- Bucketing 

create table if not exists test1.hotels_bucket (
Hotel_Address string,
Review_Date string,
 Additional_Number_of_Scoring int,
 Average_Score double,
 Hotel_Name string,
 Reviewer_Nationality string,
 Negative_Review string,
 Review_Total_Negative_Word_Counts int,
 Total_Number_of_Reviews int,
 Positive_Review string,
 Review_Total_Positive_Word_Counts int,
 Total_Number_of_Reviews_Reviewer_Has_Given int,
 Reviewer_Score double,
 days_since_review string,
 lat string,
 lng string,
 Tags string
 )
 clustered by (Hotel_Name) into 8 buckets 
row format delimited 
fields terminated by ',' 
lines terminated by '\n' 
stored as orc;


set hive.enforce.bucketing = true;

insert into test1.hotels_bucket select * from test1.hotels_orc;

describe formatted test1.hotels_bucket;

SELECT COUNT (1) from test1.hotels_bucket ;
-- 515738

/**
train@localhost big_data]$ hdfs dfs -ls /user/hive/warehouse/test1.db/hotels_bucket
Found 8 items
-rw-r--r--   1 train hive    5371070 2021-04-14 23:37 /user/hive/warehouse/test1.db/hotels_bucket/000000_0
-rw-r--r--   1 train hive    5089469 2021-04-14 23:37 /user/hive/warehouse/test1.db/hotels_bucket/000001_0
-rw-r--r--   1 train hive    4490671 2021-04-14 23:37 /user/hive/warehouse/test1.db/hotels_bucket/000002_0
-rw-r--r--   1 train hive    5557606 2021-04-14 23:37 /user/hive/warehouse/test1.db/hotels_bucket/000003_0
-rw-r--r--   1 train hive    5637617 2021-04-14 23:38 /user/hive/warehouse/test1.db/hotels_bucket/000004_0
-rw-r--r--   1 train hive    4157613 2021-04-14 23:38 /user/hive/warehouse/test1.db/hotels_bucket/000005_0
-rw-r--r--   1 train hive    6572476 2021-04-14 23:38 /user/hive/warehouse/test1.db/hotels_bucket/000006_0
-rw-r--r--   1 train hive    5416929 2021-04-14 23:38 /user/hive/warehouse/test1.db/hotels_bucket/000007_0
 */