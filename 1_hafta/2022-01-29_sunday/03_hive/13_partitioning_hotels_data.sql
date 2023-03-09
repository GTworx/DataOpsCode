--select db 
use test1;


--source table
-- Understanding schema problems
DESCRIBE test1.hotels_parquet;


/* explore the source table */
select * from test1.hotels_parquet limit 5;

select hotel_name, count(1) as total_count 
from test1.hotels_parquet 
group by hotel_name 
order by total_count desc;

select COUNT(DISTINCT hotel_name) FROM test1.hotels_parquet; 
-- 1492

select COUNT(DISTINCT review_date) FROM test1.hotels_parquet; 
-- 731



-- there are too much categories we'd better use year+month as partition 
SELECT review_date, 
MONTH(from_unixtime(unix_timestamp(review_date , 'MM/dd/yyyy'))) as review_month, 
YEAR(from_unixtime(unix_timestamp(review_date , 'MM/dd/yyyy'))) as review_year 
from test1.hotels_parquet limit 20;


drop table test1.hotels_prt ;

-- create partitioned table 
create table if not exists test1.hotels_prt (
Hotel_Address string,
Review_Date Date,
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
 partitioned by (review_year int, review_month int)
 stored as parquet ;



describe test1.hotels_prt;


-- open dynamic partitioning
set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;




-- please pay attention to partition column must be at the end in select statement
INSERT into table test1.hotels_prt PARTITION(review_year, review_month) 
select Hotel_Address,
Review_Date,
Additional_Number_of_Scoring,
 Average_Score,
 Hotel_Name,
 Reviewer_Nationality,
 Negative_Review,
 Review_Total_Negative_Word_Counts,
 Total_Number_of_Reviews,
 Positive_Review,
 Review_Total_Positive_Word_Counts,
 Total_Number_of_Reviews_Reviewer_Has_Given,
 Reviewer_Score,
 days_since_review,
 lat,
 lng,
 Tags,
 YEAR(from_unixtime(unix_timestamp(review_date , 'MM/dd/yyyy'))) as review_year,
 MONTH(from_unixtime(unix_timestamp(review_date , 'MM/dd/yyyy'))) as review_month
from test1.hotels_parquet;

-- It will take some time


SELECT count(1) from test1.hotels_prt ;
- 515738


show partitions test1.hotels_prt;
/*
partition                       |
--------------------------------+
review_year=2015/review_month=10|
review_year=2015/review_month=11|
review_year=2015/review_month=12|
review_year=2015/review_month=8 |
review_year=2015/review_month=9 |
review_year=2016/review_month=1 |
review_year=2016/review_month=10|
review_year=2016/review_month=11|
review_year=2016/review_month=12|
review_year=2016/review_month=2 |
review_year=2016/review_month=3 |
review_year=2016/review_month=4 |
review_year=2016/review_month=5 |
review_year=2016/review_month=6 |
review_year=2016/review_month=7 |
review_year=2016/review_month=8 |
review_year=2016/review_month=9 |
review_year=2017/review_month=1 |
review_year=2017/review_month=2 |
review_year=2017/review_month=3 |
review_year=2017/review_month=4 |
review_year=2017/review_month=5 |
review_year=2017/review_month=6 |
review_year=2017/review_month=7 |
review_year=2017/review_month=8 |
*/

