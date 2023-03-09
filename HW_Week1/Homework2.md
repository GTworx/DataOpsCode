### Q-1:
Create a hive database `hive_odev` and load this data https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv into `wine` table.
- Check if hiveserver2 is running
  - pgrep -f org.apache.hive.service.server.HiveServer2
- Check  if metastore is running
  - pgrep -f org.apache.hadoop.hive.metastore.HiveMetaStore
- beeline connection
  - beeline -u jdbc:hive2://127.0.0.1:10000
  - close the logs, set hive.server2.logging.operation.level=none; 
  - show databases;
- create a hive database
  - drop database hive_odev CASCADE; (if database exists)
  - create database if not exists hive_odev;
  - use hive_odev;
  - create table if not exists hive_odev.wine
  (Alcohol float,Malic_Acid float,Ash float,Ash_Alcanity float,Magnesium float,Total_Phenols float,Flavanoids float,
  Nonflavanoid_Phenols float,Proanthocyanins float,Color_Intensity float,Hue float,OD280 float,Proline float,Customer_Segment int)
  row format delimited
  fields terminated by ','
  lines terminated by '\n'
  stored as textfile
  tblproperties('skip.header.line.count'='1');
- describe hive_odev.wine;
- Load file from local to table
  - load data inpath '/user/train/hdfs_odev/Wine.csv' into table hive_odev.wine;
- See the data
  - select * from hive_odev.wine limit 3;
  
### Q-2
In `wine` table filter records that `Alcohol`greater than 13.00 then insert these records into `wine_alc_gt_13` table.
  - create table hive_odev.wine_alc_gt_13 as select * from hive_odev.wine where Alcohol > 13.00;
  - select count(1) from hive_odev.wine_alc_gt_13;
  
### Q-3
Drop `hive_odev` database including underlying tables in a single command.
  - drop database hive_odev CASCADE; 

### Q-4 
Load this https://raw.githubusercontent.com/erkansirin78/datasets/master/hive/employee.txt into table `employee` in `company` database.
- Copy file from web to local `/home/train/dataset`
  - cd /home/train/datasets
  - wget https://raw.githubusercontent.com/erkansirin78/datasets/master/hive/employee.txt
  - ls -l -t, check if the file came
  - head /home/train/dataset/employee.txt
- Copy file from local to Hdfs 
  - hdfs dfs -put ~/datasets/employee.txt /user/train/datasets
  - hdfs dfs -ls -t /user/train/datasets
  - hdfs dfs -head /user/train/datasets/employee.txt
- beeline connection
  - beeline -u jdbc:hive2://127.0.0.1:10000
  - close the logs, set hive.server2.logging.operation.level=none; 
  - show databases;
- create a company database
  - create database if not exists company;
  - use company; 
  - Create table if not exists company.employee
  (name string, work_place array<string>, 
  gender_age struct<gender:string, age:int>,
  skills_score map<string, int>)
  row format delimited
  fields terminated by '|'
  collection items terminated by ','
  map keys terminated by ':'
  lines terminated by '\n'
  stored as textfile
  tblproperties('skip.header.line.count'='1');
- Copy data from hdfs to hive
  - load data inpath '/user/train/datasets/employee.txt' into table company.employee;
- Copy data into existing table, delete and insert
  - load data inpath '/user/train/datasets/employee.txt' overwrite into table company.employee;
  - select * from company.employee;
### Q-5
Write a query that returns the employees whose Python skill is greater than 70.
  - select * from company.employee where skills_score["Python"] > 70;
Write a query to filter struct
  - select * from company.employee where gender_age.gender = "Male"; 
  - select * from company.employee where gender_age.age >= 30;

