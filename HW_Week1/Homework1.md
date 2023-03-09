### Q-1: 
Download and put `https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv` dataset in hdfs `/user/train/hdfs_odev` directory.

- Start virtual machine
- Connect through MobaXterm
- Check the web ui to see if it is up http://localhost:9870/
- Create a new directory 
    - hdfs dfs -mkdir /user/train/hdfs_odev
    - run hdfs dfs -ls -t /user/train, (-t sorts the list by modification time)
- Copy file to local `/home/train/dataset`
  - cd /home/train/datasets
  - wget https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv
  - ls -l -t, check if the file came
- Put file from local to hdfs
  - hdfs dfs -put ~/datasets/Wine.csv /user/train/hdfs_odev
  - hdfs dfs -ls -t /user/train/hdfs_odev
  - hdfs dfs -head /user/train/hdfs_odev/Wine.csv
  - hdfs dfs -put ~/datasets/Wine.csv /user/train/hdfs_odev/Wine2.csv

### Q-2:
Copy this hdfs file `/user/train/hdfs_odev/Wine.csv` to `/tmp/hdfs_odev` hdfs directory.
  - hdfs dfs -mkdir /tmp/hdfs_odev
  - hdfs dfs -ls -t /tmp/
  - hdfs dfs -cp /user/train/hdfs_odev/Wine.csv /tmp/hdfs_odev
  - hdfs dfs -ls -t /tmp/hdfs_odev
  - hdfs dfs -head /tmp/hdfs_odev/Wine.csv

### Q-3:
Delete `/tmp/hdfs_odev` directory with skipping the trash. 
  - hdfs dfs -rm -r -skipTrash /tmp/hdfs_odev

### Q-4:
Explore `/user/train/hdfs_odev/Wine.csv` file from web hdfs.
  - http://localhost:9870/, go to utilities => Browse the file system
  - click to user, train, hdfs_odev
  - download, head, tail did not work
  - delete works