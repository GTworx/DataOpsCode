### Q-1: 
- Download and put `https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv` dataset in hdfs `/home/train/hdfs_odev` directory.

[train@trainvm ~]$ cd Downloads/
[train@trainvm Downloads]$ ll
total 58600
-rw-rw-r--. 1 train train 60005232 Jul 20  2020 dbeaver-ce-latest-stable.x86_64.rpm
[train@trainvm Downloads]$ wget https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv
--2023-02-02 00:33:47--  https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.110.133, 185.199.111.133, 185.199.108.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.110.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 11284 (11K) [text/plain]
Saving to: ‘Wine.csv’

100%[=================================================================================>] 11,284      --.-K/s   in 0.002s

2023-02-02 00:33:47 (5.98 MB/s) - ‘Wine.csv’ saved [11284/11284]

[train@trainvm Downloads]$ ll
total 58612
-rw-rw-r--. 1 train train 60005232 Jul 20  2020 dbeaver-ce-latest-stable.x86_64.rpm
-rw-rw-r--. 1 train train    11284 Feb  2 00:33 Wine.csv
[train@trainvm ~]$ hdfs dfs -mkdir /user/train/hdfs_odev
[train@trainvm Downloads]$ hdfs dfs -put Wine.csv /user/train/hdfs_odev
[train@trainvm Downloads]$ hdfs dfs -ls /user/train/hdfs_odev
Found 1 items
-rw-r--r--   1 train supergroup      11284 2023-02-02 00:34 /user/train/hdfs_odev/Wine.csv

### Q-2:
- Copy this hdfs file `/user/train/hdfs_odev/Wine.csv` to `/tmp/hdfs_odev` hdfs directory.

[train@trainvm ~]$ hdfs dfs -ls /tmp
Found 4 items
drwx------   - train supergroup          0 2020-09-23 19:48 /tmp/hadoop-yarn
drwx-wx-wx   - train supergroup          0 2020-09-23 18:17 /tmp/hive
drwxr-xr-x   - train supergroup          0 2020-11-25 08:21 /tmp/mlflow
drwxr-xr-x   - train supergroup          0 2020-11-21 12:43 /tmp/temporary-0a4e530a-ab2d-47db-9f7a-a4c79a9d4221
[train@trainvm ~]$ hdfs dfs -mkdir /tmp/hdfs_odev
[train@trainvm ~]$ hdfs dfs -cp /user/train/hdfs_odev/Wine.csv /tmp/hdfs_odev
[train@trainvm ~]$ hdfs dfs -ls /tmp/hdfs_odev
Found 1 items
-rw-r--r--   1 train supergroup      11284 2023-02-02 00:39 /tmp/hdfs_odev/Wine.csv

### Q-3:
- Delete `/tmp/hdfs_odev` directory with skipping the trash. 

[train@trainvm ~]$ hdfs dfs -rm -R -skipTrash /tmp/hdfs_odev
Deleted /tmp/hdfs_odev
[train@trainvm ~]$ hdfs dfs -ls /tmp
Found 4 items
drwx------   - train supergroup          0 2020-09-23 19:48 /tmp/hadoop-yarn
drwx-wx-wx   - train supergroup          0 2020-09-23 18:17 /tmp/hive
drwxr-xr-x   - train supergroup          0 2020-11-25 08:21 /tmp/mlflow
drwxr-xr-x   - train supergroup          0 2020-11-21 12:43 /tmp/temporary-0a4e530a-ab2d-47db-9f7a-a4c79a9d4221

### Q-4:
-  Explore `/user/train/hdfs_odev/Wine.csv` file from web hdfs.  

