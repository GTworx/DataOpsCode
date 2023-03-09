#Preparations

1. Check Spark installation location
```
ls -l /opt/manual/spark/
```

2. Spark needs Java and Python, check their version. Also there is web ui ```http://localhost:4040/```
```
java --version
python -V
python3 -V
```

3. Go to  shell, note the version , use ```quit()``` to leave the shell when needed.
```
pyspark
```

4. Create a new directory and go there
```
mkdir /home/train/dataops7
mkdir /home/train/dataops7/spark
mkdir /home/train/dataops7/spark/hw3_DataCleaning
cd /home/train/dataops7/spark/hw3_DataCleaning
```
5. We need a virtual environment, with pyspark installed. It should have the same version as notes in the step 3. 

6. Activate the already existing ```venvspark``` virtual environment. You can use ```deactivate``` command to close it when needed.
```
source /home/train/venvspark/bin/activate
```
6. We will use jupyterlab for coding (you can also use pycharm if you want). Install the package. 
```
pip install jupyterlab
```
7. To run jupyter notebook from the main browser 
   1. make the port forwarding in the virtual box, ```8888 to 8888```
   2. start jupyter lab ```jupyter lab --ip 0.0.0.0 --port 8888```
   3. copy the link, token part of it, after jupyter lab starts. Note that token changes every new run. 
   4. You can close Jupyter lab with ```CTRL-C``` when needed.
   

8. Start hadoop with ```start-all.sh```, (stop with ```stop-all.sh``` when needed)
   1. check hiveserver2 running ```pgrep -f org.apache.hive.service.server.HiveServer2```
   2. check metastore running ```pgrep -f org.apache.hadoop.hive.metastore.HiveMetaStore```
   3. start beeline ```beeline -u jdbc:hive2://127.0.0.1:10000```
   4. close the logs, ```set hive.server2.logging.operation.level=none;``` 
   5. stop beeline ```CTRL-D``` when needed

   
9. Check PostGre by running from the shell with
```
psql -h host -d traindb -U train -W
psql -d traindb -U train
```
10. Some good to know commands in psql 
    1. shows databases ```\l```
    2. switch to another db ```\c traindb```
    3. show all tables ```\dt```
    4. describe table ```\d table_name```
    5. list all views ```\dv```
    6. help ```\?```
    7. quit ```\q```
    

10. Make connection to PostGre from DBeaver either within the virtual box or from host machine. 
if used from host machine, do the port forwarding ```5432 to 5432``` first.

    1. ip ```LocalHost```
    2. port ```5432```
    3. database ```traindb```
    4. user ```train```
    5. password ```Ankara06```

# Notes

When creating spark session, if you have master as YARN, don't forget to start hadoop first. 
Otherwise, Spark session will not be created properly.

could not manage to save to hive with file type txt/csv, check this later


