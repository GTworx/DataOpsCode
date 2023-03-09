## 1. Install mysql
- create a script that installs mysql-server
```
cat install_mysql.sh

#!/bin/bash
sudo yum update
wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
sudo rpm -Uvh mysql80-community-release-el7-3.noarch.rpm
sudo yum install mysql-server
sudo systemctl start mysqld
```

- Make script file executable
` chmod +x install_mysql.sh `  

- Install 
` ./install_mysql.sh `  
From time to time script will ask for sudo password and y confirmations.

- Check if mysql-server is running
` sudo systemctl status mysqld `  

- Learn root password
```
[train@localhost my_big-data]$ sudo grep 'password' /var/log/mysqld.log
2021-02-07T16:07:50.331974Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: Smes!Lgp>5xI
```

- Change root password and secure your installation follow the instructions.
` sudo mysql_secure_installation `

- Connect to mysql shell
` mysql -u root -p `  

- https://www.hostinger.web.tr/rehberler/centos-7de-mysql-kurulumu/

## 2. sqoop incermental load
- Learn MySQL verision
```
[train@localhost my_big-data]$ mysql -V
mysql  Ver 8.0.23 for Linux on x86_64 (MySQL Community Server - GPL)
```
- Download mysql driver
```
wget -P /opt/manual/sqoop/lib/ https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.23/mysql-connector-java-8.0.23.jar


[train@localhost my_big-data]$ ls -l /opt/manual/sqoop/lib/ | grep mysql
-rw-rw-r--. 1 train train 2415211 Dec  1 19:29 mysql-connector-java-8.0.23.jar
```
- Connect mysql shell
`mysql -uroot `  

- Create and select a database
```
mysql> create database traindb;
Query OK, 1 row affected (0.01 sec)

mysql> use traindb;
Database changed
```

- Create a table
```
CREATE TABLE stocks (
id INT NOT NULL AUTO_INCREMENT,
symbol varchar(10), 
name varchar(40), 
trade_date DATE, 
close_price DOUBLE, 
volume INT,
updated_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,
PRIMARY KEY ( id )
);
```

- Insert record into stocks table
```
INSERT INTO stocks 
(symbol, name, trade_date, close_price, volume)
VALUES
('AAL', 'American Airlines', '2015-11-12', 42.4, 4404500);

INSERT INTO stocks 
(symbol, name, trade_date, close_price, volume)
VALUES
('AAPL', 'Apple', '2015-11-12', 115.23, 40217300);

INSERT INTO stocks 
(symbol, name, trade_date, close_price, volume)
VALUES
('AMGN', 'Amgen', '2015-11-12', 157.0, 1964900);
```

- Check results
```
mysql> select * from stocks;
+----+--------+-------------------+------------+-------------+----------+---------------------+
| id | symbol | name              | trade_date | close_price | volume   | updated_time        |
+----+--------+-------------------+------------+-------------+----------+---------------------+
|  1 | AAL    | American Airlines | 2015-11-12 |        42.4 |  4404500 | 2021-02-07 19:25:35 |
|  2 | AAPL   | Apple             | 2015-11-12 |      115.23 | 40217300 | 2021-02-07 19:25:35 |
|  3 | AMGN   | Amgen             | 2015-11-12 |         157 |  1964900 | 2021-02-07 19:25:35 |
+----+--------+-------------------+------------+-------------+----------+---------------------+
```

- Create train user and grant privileges on traindb database
```
mysql> CREATE USER 'train'@'%' IDENTIFIED BY 'Mrk23+??-is';
Query OK, 0 rows affected (0.02 sec)

mysql> GRANT ALL PRIVILEGES ON traindb.* TO 'train'@'%' WITH GRANT OPTION;
Query OK, 0 rows affected (0.00 sec)
```

- Create and execute a Sqoop job with incremental append option  
```
sqoop job --create incrementalappendImportJob --import \
--connect jdbc:mysql://localhost/traindb \
--driver com.mysql.jdbc.Driver \
--username train --password Mrk23+??-is  \
--table stocks --target-dir /user/train/sqoop/stocks_append \
--incremental append --check-column id -m 1


Warning: /opt/manual/sqoop//../hbase does not exist! HBase imports will fail.
Please set $HBASE_HOME to the root of your HBase installation.
Warning: /opt/manual/sqoop//../hcatalog does not exist! HCatalog jobs will fail.
Please set $HCAT_HOME to the root of your HCatalog installation.
Warning: /opt/manual/sqoop//../accumulo does not exist! Accumulo imports will fail.
Please set $ACCUMULO_HOME to the root of your Accumulo installation.
2021-02-07 19:50:02,318 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6
2021-02-07 19:50:03,194 WARN tool.BaseSqoopTool: Setting your password on the command-line is insecure. Consider using -P instead.
```

- List jobs
```
[train@localhost my_big-data]$ sqoop job --list

2021-02-07 19:51:10,333 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6
Available jobs:
  incrementalappendImportJob
```

- See the details of the job
```
[train@localhost my_big-data]$ sqoop job --show incrementalappendImportJob

2021-02-07 19:52:43,679 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6
Enter password:
Job: incrementalappendImportJob
Tool: import
Options:
----------------------------
verbose = false
db.connect.string = jdbc:mysql://localhost/traindb
codegen.output.delimiters.escape = 0
codegen.output.delimiters.enclose.required = false
codegen.input.delimiters.field = 0
hbase.create.table = false
db.require.password = true
hdfs.append.dir = true
db.table = stocks
codegen.input.delimiters.escape = 0
import.fetch.size = null
accumulo.create.table = false
codegen.input.delimiters.enclose.required = false
db.username = train
reset.onemapper = false
codegen.output.delimiters.record = 10
import.max.inline.lob.size = 16777216
hbase.bulk.load.enabled = false
hcatalog.create.table = false
db.clear.staging.table = false
incremental.col = id
codegen.input.delimiters.record = 0
enable.compression = false
hive.overwrite.table = false
hive.import = false
codegen.input.delimiters.enclose = 0
accumulo.batch.size = 10240000
hive.drop.delims = false
codegen.output.delimiters.enclose = 0
hdfs.delete-target.dir = false
codegen.output.dir = .
codegen.auto.compile.dir = true
relaxed.isolation = false
mapreduce.num.mappers = 1
accumulo.max.latency = 5000
import.direct.split.size = 0
codegen.output.delimiters.field = 44
export.new.update = UpdateOnly
incremental.mode = AppendRows
hdfs.file.format = TextFile
codegen.compile.dir = /tmp/sqoop-train/compile/48b70ca35e538db6144c052607fa3a9d
direct.import = false
hdfs.target.dir = /user/train/sqoop/stocks_append
```

- Execute the Sqoop job and observe the records written to HDFS
` sqoop job --exec incrementalappendImportJob  ` 

- Check hdfs 
```
[train@localhost my_big-data]$ hdfs dfs -cat /user/train/sqoop/stocks_append/part-m-00000
1,AAL,American Airlines,2015-11-12,42.4,4404500,2021-02-07 19:25:35.0
2,AAPL,Apple,2015-11-12,115.23,40217300,2021-02-07 19:25:35.0
3,AMGN,Amgen,2015-11-12,157.0,1964900,2021-02-07 19:25:35.0
```

-  Insert values in the source table

```
INSERT INTO stocks 
(symbol, name, trade_date, close_price, volume)
VALUES
('GARS', 'Garrison', '2015-11-12', 12.4, 23500);

INSERT INTO stocks 
(symbol, name, trade_date, close_price, volume)
VALUES
('SBUX', 'Starbucks', '2015-11-12', 62.90, 4545300);

INSERT INTO stocks 
(symbol, name, trade_date, close_price, volume)
VALUES
('SGI', 'Silicon Graphics', '2015-11-12', 4.12, 123200);
```
- Check
```
select * from stocks;
+----+--------+-------------------+------------+-------------+----------+---------------------+
| id | symbol | name              | trade_date | close_price | volume   | updated_time        |
+----+--------+-------------------+------------+-------------+----------+---------------------+
|  1 | AAL    | American Airlines | 2015-11-12 |        42.4 |  4404500 | 2021-02-07 19:25:35 |
|  2 | AAPL   | Apple             | 2015-11-12 |      115.23 | 40217300 | 2021-02-07 19:25:35 |
|  3 | AMGN   | Amgen             | 2015-11-12 |         157 |  1964900 | 2021-02-07 19:25:35 |
|  4 | GARS   | Garrison          | 2015-11-12 |        12.4 |    23500 | 2021-02-07 22:14:04 |
|  5 | SBUX   | Starbucks         | 2015-11-12 |        62.9 |  4545300 | 2021-02-07 22:14:04 |
|  6 | SGI    | Silicon Graphics  | 2015-11-12 |        4.12 |   123200 | 2021-02-07 22:14:05 |
+----+--------+-------------------+------------+-------------+----------+---------------------+
```

- Execute the Sqoop job again and observe the output in HDFS
`  sqoop job --exec incrementalappendImportJob  ` 

- See new records in hdfs 
```
[train@localhost my_big-data]$ hdfs dfs -cat /user/train/sqoop/stocks_append/part-m-00000
1,AAL,American Airlines,2015-11-12,42.4,4404500,2021-02-07 19:25:35.0
2,AAPL,Apple,2015-11-12,115.23,40217300,2021-02-07 19:25:35.0
3,AMGN,Amgen,2015-11-12,157.0,1964900,2021-02-07 19:25:35.0
[train@localhost my_big-data]$ hdfs dfs -cat /user/train/sqoop/stocks_append/part-m-00001
4,GARS,Garrison,2015-11-12,12.4,23500,2021-02-07 22:14:04.0
5,SBUX,Starbucks,2015-11-12,62.9,4545300,2021-02-07 22:14:04.0
6,SGI,Silicon Graphics,2015-11-12,4.12,123200,2021-02-07 22:14:05.0
```
- See the metadata (incremental.last.value = 6)
```
[train@localhost my_big-data]$ sqoop job --show incrementalappendImportJob | grep incremental
2021-02-07 22:18:38,656 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6
2021-02-07 22:18:39,593 ERROR sqoop.SqoopOptions: It seems that you have launched a Sqoop metastore job via
2021-02-07 22:18:39,593 ERROR sqoop.SqoopOptions: Oozie with sqoop.metastore.client.record.password disabled.
2021-02-07 22:18:39,593 ERROR sqoop.SqoopOptions: But this configuration is not supported because Sqoop can't
2021-02-07 22:18:39,593 ERROR sqoop.SqoopOptions: prompt the user to enter the password while being executed
2021-02-07 22:18:39,594 ERROR sqoop.SqoopOptions: as Oozie tasks. Please enable sqoop.metastore.client.record
2021-02-07 22:18:39,594 ERROR sqoop.SqoopOptions: .password in sqoop-site.xml, or provide the password
2021-02-07 22:18:39,594 ERROR sqoop.SqoopOptions: explicitly using --password in the command tag of the Oozie
2021-02-07 22:18:39,594 ERROR sqoop.SqoopOptions: workflow file.
Job: incrementalappendImportJob
incremental.last.value = 6
incremental.col = id
incremental.mode = AppendRows
```

# Incremental Last Modified
- Create Incremental Last Modified Job  

We use --incremental lastmodified option instead of append
```
sqoop job --create incrementalImportModifiedJob -- import \
--connect jdbc:mysql://localhost/traindb \
--driver com.mysql.jdbc.Driver \
--username train --password Mrk23+??-is  \
--table stocks --target-dir /user/train/sqoop/stocks_modified  \
--incremental lastmodified --check-column updated_time -m 1 --append
```

- Observe metadata information in job
Observe incremental.mode is set to DateLastModified and incremental.col is set to updated_time
` sqoop job --show incrementalImportModifiedJob `  

- Execute the Sqoop Job and observe the metadata information
` sqoop job --exec incrementalImportModifiedJob ` 

- See result in hdfs
```
 hdfs dfs -cat /user/train/sqoop/stocks_modified/part-m-00000
1,AAL,American Airlines,2015-11-12,42.4,4404500,2021-02-07 19:25:35.0
2,AAPL,Apple,2015-11-12,115.23,40217300,2021-02-07 19:25:35.0
3,AMGN,Amgen,2015-11-12,157.0,1964900,2021-02-07 19:25:35.0
4,GARS,Garrison,2015-11-12,12.4,23500,2021-02-07 22:14:04.0
5,SBUX,Starbucks,2015-11-12,62.9,4545300,2021-02-07 22:14:04.0
6,SGI,Silicon Graphics,2015-11-12,4.12,123200,2021-02-07 22:14:05.
```

- Modify Data in the source table
We update two rows and insert three new rows , in total there are five changes.
```
UPDATE stocks SET volume = volume+100, updated_time=now() WHERE id in (2,3);

INSERT INTO stocks 
(symbol, name, trade_date, close_price, volume)
VALUES
('GARS', 'Garrison', '2015-11-12', 12.4, 23500);

INSERT INTO stocks 
(symbol, name, trade_date, close_price, volume)
VALUES
('SBUX', 'Starbucks', '2015-11-12', 62.90, 4545300);

INSERT INTO stocks 
(symbol, name, trade_date, close_price, volume)
VALUES
('SGI', 'Silicon Graphics', '2015-11-12', 4.12, 123200);
```

- Execute the Sqoop Job and observe the metadata information
` sqoop job --exec incrementalImportModifiedJob `

- See result in hdfs
```
hdfs dfs -cat /user/train/sqoop/stocks_modified/part-m-00001
2,AAPL,Apple,2015-11-12,115.23,40217400,2021-02-07 22:40:25.0
3,AMGN,Amgen,2015-11-12,157.0,1965000,2021-02-07 22:40:25.0
7,GARS,Garrison,2015-11-12,12.4,23500,2021-02-07 22:40:37.0
8,SBUX,Starbucks,2015-11-12,62.9,4545300,2021-02-07 22:40:37.0
9,SGI,Silicon Graphics,2015-11-12,4.12,123200,2021-02-07 22:40:38.0
```


-  Merge Changes
We have retrieved records that have changed , but this is not the expected result as we need to merge the changes.  

```
sqoop codegen --connect jdbc:mysql://localhost/traindb \
--driver com.mysql.jdbc.Driver \
--username train --password Mrk23+??-is  \
--table stocks --outdir /home/train/my_big_data/sqoop-codegen-stocks
```
- move generated jar to your directory
`  mv /tmp/sqoop-train/compile/6d9d483ee2325910d060b56183e6bfae/stocks.jar .  `  

```
sqoop merge --new-data /user/train/sqoop/stocks_modified/part-m-00001 \
--onto /user/train/sqoop/stocks_modified/part-m-00000 \
--target-dir /user/train/sqoop/stocks_modified/merged \
--jar-file stocks.jar --class-name stocks --merge-key id
```

- Observe output in the Merged directory
```
[train@localhost my_big-data]$ hdfs dfs -cat /user/train/sqoop/stocks_modified/merged/part-r-00000
1,AAL,American Airlines,2015-11-12,42.4,4404500,2021-02-07 19:25:35.0
2,AAPL,Apple,2015-11-12,115.23,40217400,2021-02-07 22:40:25.0
3,AMGN,Amgen,2015-11-12,157.0,1965000,2021-02-07 22:40:25.0
4,GARS,Garrison,2015-11-12,12.4,23500,2021-02-07 22:14:04.0
5,SBUX,Starbucks,2015-11-12,62.9,4545300,2021-02-07 22:14:04.0
6,SGI,Silicon Graphics,2015-11-12,4.12,123200,2021-02-07 22:14:05.0
7,GARS,Garrison,2015-11-12,12.4,23500,2021-02-07 22:40:37.0
8,SBUX,Starbucks,2015-11-12,62.9,4545300,2021-02-07 22:40:37.0
9,SGI,Silicon Graphics,2015-11-12,4.12,123200,2021-02-07 22:40:38.0
```






















- https://medium.com/datadriveninvestor/incremental-data-load-using-apache-sqoop-3c259308f65c
