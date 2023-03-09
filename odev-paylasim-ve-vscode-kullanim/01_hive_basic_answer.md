# 1. Hafta Hive Ödev Çözümleri

## Hive Servislerinin Kontrol Edilmesi

```
pgrep -f org.apache.hive.service.server.HiveServer2
```

```
pgrep -f org.apache.hadoop.hive.metastore.HiveMetaStore
```

> Eğer yukarıdaki komutlardan herhangi biri sayı döndürmüyorsa aşağıdaki komut kullanılır.

**Komut:**

```
start-all.sh
```

**Beklenen Çıktı:**

```
WARNING: Attempting to start all Apache Hadoop daemons as train in 10 seconds.
WARNING: This is not a recommended production deployment configuration.
WARNING: Use CTRL-C to abort.
Starting namenodes on [localhost]
Starting datanodes
Starting secondary namenodes [trainvm.vbo.local]
WARNING: YARN_CONF_DIR has been replaced by HADOOP_CONF_DIR. Using value of YARN_CONF_DIR.
Starting resourcemanager
WARNING: YARN_CONF_DIR has been replaced by HADOOP_CONF_DIR. Using value of YARN_CONF_DIR.
Starting nodemanagers
WARNING: YARN_CONF_DIR has been replaced by HADOOP_CONF_DIR. Using value of YARN_CONF_DIR.
localhost: WARNING: YARN_CONF_DIR has been replaced by HADOOP_CONF_DIR. Using value of YARN_CONF_DIR.
Hive is starting...
Hive started
```

Servisler başladıktan sonra çözümlerimizi gerçekleştirebiliriz.

## Soru 1-3

- Create a hive database `hive_odev` and load this data https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv into `wine` table.
- In `wine` table filter records that `Alcohol`greater than 13.00 then insert these records into `wine_alc_gt_13` table.
- Drop `hive_odev` database including underlying tables in a single command.

## Çözüm 1-3

### Dosyanın İndirilmesi

**Komut:**

```
wget -P ~/datasets/ https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv
```

**Beklenen Çıktı:**

```
--2023-02-02 18:11:20--  https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.110.133, 185.199.111.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 11284 (11K) [text/plain]
Saving to: ‘/home/train/datasets/Wine.csv’

100%[================================================================================================================>] 11,284      --.-K/s   in 0.003s

2023-02-02 18:11:20 (3.43 MB/s) - ‘/home/train/datasets/Wine.csv’ saved [11284/11284]
```

**Komut:**

```
ls -l ~/datasets/
```

**Beklenen Çıktı:**

```
total 28
-rw-rw-r--. 1 train train  4556 Jul 21  2020 Advertising.csv
drwxr-xr-x. 3 train train    96 Nov 19  2020 churn-telecom
-rw-rw-r--. 1 train train  4611 Nov 20  2020 iris.csv
drwxrwxr-x. 2 train train   133 Jul 23  2020 retail_db
-rw-rw-r--. 1 train train 11284 Feb  2 18:11 Wine.csv
```

**Komut:**

```
head datasets/Wine.csv
```

**Beklenen Çıktı:**

```
Alcohol,Malic_Acid,Ash,Ash_Alcanity,Magnesium,Total_Phenols,Flavanoids,Nonflavanoid_Phenols,Proanthocyanins,Color_Intensity,Hue,OD280,Proline,Customer_Segment
14.23,1.71,2.43,15.6,127,2.8,3.06,0.28,2.29,5.64,1.04,3.92,1065,1
13.2,1.78,2.14,11.2,100,2.65,2.76,0.26,1.28,4.38,1.05,3.4,1050,1
13.16,2.36,2.67,18.6,101,2.8,3.24,0.3,2.81,5.68,1.03,3.17,1185,1
14.37,1.95,2.5,16.8,113,3.85,3.49,0.24,2.18,7.8,0.86,3.45,1480,1
13.24,2.59,2.87,21,118,2.8,2.69,0.39,1.82,4.32,1.04,2.93,735,1
14.2,1.76,2.45,15.2,112,3.27,3.39,0.34,1.97,6.75,1.05,2.85,1450,1
14.39,1.87,2.45,14.6,96,2.5,2.52,0.3,1.98,5.25,1.02,3.58,1290,1
14.06,2.15,2.61,17.6,121,2.6,2.51,0.31,1.25,5.05,1.06,3.58,1295,1
14.83,1.64,2.17,14,97,2.8,2.98,0.29,1.98,5.2,1.08,2.85,1045,1
```

### HDFS'te İstenen Klasörün Oluşturulması

**Komut:**

```
hdfs dfs -ls /user/train
```

**Beklenen Çıktı:**

```
Found 11 items
drwx------   - train supergroup          0 2021-11-03 22:40 /user/train/.flink
drwxr-xr-x   - train supergroup          0 2023-02-02 00:05 /user/train/.sparkStaging
drwxr-xr-x   - train supergroup          0 2023-02-02 07:50 /user/train/datasets
drwxr-xr-x   - train supergroup          0 2020-11-22 11:04 /user/train/exactly_once_guarantee
drwxr-xr-x   - train supergroup          0 2020-11-22 12:22 /user/train/loans_delta
drwxr-xr-x   - train supergroup          0 2020-11-25 08:35 /user/train/mlflow
drwxr-xr-x   - train supergroup          0 2023-02-01 23:54 /user/train/play-hdfs-commands
drwxr-xr-x   - train supergroup          0 2020-11-20 07:44 /user/train/read_from_kafka
drwxr-xr-x   - train supergroup          0 2020-11-22 13:41 /user/train/saved_models
drwxr-xr-x   - train supergroup          0 2020-11-21 12:53 /user/train/wordCountCheckpoint
drwxr-xr-x   - train supergroup          0 2020-11-22 11:57 /user/train/write_to_kafka
```

**Komut:**

```
hdfs dfs -mkdir /user/train/hdfs_odev
```

**Komut:**

```
hdfs dfs -ls /user/train
```

**Beklenen Çıktı:**

```
Found 12 items
...
drwxr-xr-x   - train supergroup          0 2023-02-02 18:29 /user/train/hdfs_odev
...
```

### HDFS'e Dosyanın Gönderilmesi

**Komut:**

```
hdfs dfs -put ~/datasets/Wine.csv /user/train/hdfs_odev
```


**Komut:**

```
hdfs dfs -ls /user/train/hdfs_odev
```

**Beklenen Çıktı:**

```
Found 1 items
-rw-r--r--   1 train supergroup      11284 2023-02-02 18:31 /user/train/hdfs_odev/Wine.csv
```

### Sorgunun eklenmesi

```
cd ~/dataops7/hive
```

```
touch hive_wine_queries.sql
```

- `vim hive_wine_queries.sql` komutu ile aşağıdaki kodları ekleyelim.

```sql
-- ############ Soru 1 Başlangıç ############

-- Logları görmezden gelir
set hive.server2.logging.operation.level=NONE;

-- Mevcut veritabanlarını göster
show databases;

-- hive_odev veritabanı oluşturma
create database hive_odev;

-- Mevcut veritabanlarını göster
show databases;

-- hive_odev veritabanını kullanma
use hive_odev;

-- wine tablosunun oluşturulması
create table if not exists hive_odev.wine (
    Alcohol float, 
    Malic_Acid float, 
    Ash float, 
    Ash_Alcanity float, 
    Magnesium float, 
    Total_Phenols float, 
    Flavanoids float, 
    Nonflavanoid_Phenols float, 
    Proanthocyanins float, 
    Color_Intensity float, 
    Hue float, 
    OD280 float, 
    Proline float, 
    Customer_Segment int)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
tblproperties('skip.header.line.count'='1');

-- wine tablosuna dosya ile veri ekleme
load data inpath '/user/train/hdfs_odev/Wine.csv' into table hive_odev.wine;

-- tablonun getirilmesi
select * from hive_odev.wine limit 10;

-- ############ Soru 1 Bitiş ############

-- ############ Soru 2 Başlangıç ############

create table hive_odev.wine_alc_gt_13 as select * from hive_odev.wine where alcohol > 13.00;

select * from hive_odev.wine limit 10;

-- ############ Soru 2 Bitiş ############

-- ############ Soru 3 Başlangıç ############

drop database hive_odev cascade;

-- Mevcut veritabanlarını göster
show databases;

-- ############ Soru 3 Bitiş ############
```

### Sorgunun Gönderilmesi

```
beeline -n train -u jdbc:hive2://localhost:10000 -f ./hive_wine_queries.sql
```

## Soru 4-5

- Load this https://raw.githubusercontent.com/erkansirin78/datasets/master/hive/employee.txt into table `employee` in `company` database. 
- Write a query that returns the employees whose Python skill is greater than 70.

## Çözüm 4-5

### Dosyanın İndirilmesi

**Komut:**

```
wget -P ~/datasets/ https://raw.githubusercontent.com/erkansirin78/datasets/master/hive/employee.txt
```

**Beklenen Çıktı:**

```
--2023-02-02 20:06:16--  https://raw.githubusercontent.com/erkansirin78/datasets/master/hive/employee.txt
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.111.133, 185.199.108.133, 185.199.109.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.111.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 215 [text/plain]
Saving to: ‘/home/train/datasets/employee.txt’

100%[================================================================================================================>] 215         --.-K/s   in 0s

2023-02-02 20:06:16 (13.6 MB/s) - ‘/home/train/datasets/employee.txt’ saved [215/215]
```

**Komut:**

```
ls -l ~/datasets/
```

**Beklenen Çıktı:**

```
total 32
-rw-rw-r--. 1 train train  4556 Jul 21  2020 Advertising.csv
drwxr-xr-x. 3 train train    96 Nov 19  2020 churn-telecom
-rw-rw-r--. 1 train train   215 Feb  2 20:06 employee.txt
-rw-rw-r--. 1 train train  4611 Nov 20  2020 iris.csv
drwxrwxr-x. 2 train train   133 Jul 23  2020 retail_db
-rw-rw-r--. 1 train train 11284 Feb  2 18:11 Wine.csv
```

**Komut:**

```
head datasets/employee.txt
```

**Beklenen Çıktı:**

```
name|work_place|gender_age|skills_score
Michael|Montreal,Toronto|Male,30|DB:80,Network:88
Will|Montreal|Male,35|Perl:85,Scala:82
Shelley|New York|Female,27|Python:80,Spark:95
Lucy|Vancouver|Female,57|Sales:89,HR:94
```

### HDFS'e Dosyanın Gönderilmesi

**Komut:**

```
hdfs dfs -put ~/datasets/employee.txt /user/train/hdfs_odev
```


**Komut:**

```
hdfs dfs -ls /user/train/hdfs_odev
```

**Beklenen Çıktı:**

```
Found 1 items
-rw-r--r--   1 train supergroup        215 2023-02-02 20:07 /user/train/hdfs_odev/employee.txt
```

### Sorgunun eklenmesi

```
cd ~/dataops7/hive
```

```
touch hive_employee_queries.sql
```

- `vim hive_employee_queries.sql` komutu ile aşağıdaki kodları ekleyelim.

```sql
-- ############ Soru 4 Başlangıç ############

-- Logları görmezden gelir
set hive.server2.logging.operation.level=NONE;

-- Mevcut veritabanlarını göster
show databases;

-- company veritabanı oluşturma
create database company;

-- Mevcut veritabanlarını göster
show databases;

-- company veritabanını kullanma
use company;

-- employee tablosunun oluşturulması
create table if not exists company.employee (
    name string,
    work_place array<string>,
    gender_age struct<gender:string,age:int>,
    skills_score map<string,int>
)
row format delimited
fields terminated by '|'
collection items terminated by ','
map keys terminated by ':'
stored as textfile
tblproperties('skip.header.line.count'='1');

-- wine tablosuna dosya ile veri ekleme
load data inpath '/user/train/hdfs_odev/employee.txt' into table company.employee;

select * from company.employee limit 10;

-- ############ Soru 4 Bitiş ############

-- ############ Soru 5 Başlangıç ############

select * from company.employee where skills_score["Python"] > 70;

-- ############ Soru 5 Bitiş ############
```

### Sorgunun Gönderilmesi

```
beeline -n train -u jdbc:hive2://localhost:10000 -f ./hive_employee_queries.sql
```
