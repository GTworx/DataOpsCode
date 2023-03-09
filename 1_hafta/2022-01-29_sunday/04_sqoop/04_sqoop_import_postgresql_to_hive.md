1. We will import from postgresql traindb churn table to hive test1 database churn as table
```
sqoop import --connect jdbc:postgresql://localhost/traindb  \
--driver org.postgresql.Driver \
--username train --password Ankara06 \
--query "select * from churn WHERE \$CONDITIONS" \
--m 4 --split-by rownumber \
--hive-import  --create-hive-table --hive-table test1.churn \
--target-dir /tmp/churn
```

2. Check result from DBeaver
```
describe churn;
col_name       |data_type|comment|
---------------|---------|-------|
rownumber      |int      |       |
customerid     |int      |       |
surname        |string   |       |
creditscore    |int      |       |
geography      |string   |       |
gender         |string   |       |
age            |int      |       |
tenure         |int      |       |
balance        |double   |       |
numofproducts  |int      |       |
hascrcard      |int      |       |
isactivemember |int      |       |
estimatedsalary|double   |       |
exited         |int      |       |

select count(1) from churn;
_c0  |
-----|
10000|

```

- Note-1: If you want to import the results of a query in parallel, then each map task will need to execute a copy of the query, with results partitioned by bounding conditions inferred by Sqoop. Your query must include the token `$CONDITIONS` which each Sqoop process will replace with a unique condition expression. You must also select a splitting column with --split-by.

- Note-2: When importing a free-form query, you must specify a destination directory with --target-dir.

2. to overwrite existing table just replace `--create-hive-table` with `--hive-overwrite` and change target-dir or
delete before job

```
sqoop import --connect jdbc:postgresql://localhost/traindb  \
--driver org.postgresql.Driver \
--username train --password Ankara06 \
--query "select * from churn WHERE \$CONDITIONS" \
--m 4 --split-by rownumber \
--hive-import --hive-overwrite  --hive-table test1.churn \
--delete-target-dir --target-dir /tmp/churn
```

3. Append existing table 

```
sqoop import --connect jdbc:postgresql://localhost/traindb  \
--driver org.postgresql.Driver \
--username train --password Ankara06 \
--query "select * from churn WHERE \$CONDITIONS" \
--m 4 --split-by rownumber \
--hive-import  --hive-table test1.churn \
--delete-target-dir --target-dir /tmp/churn
```

4. import with table name
```
 sqoop import --connect jdbc:postgresql://localhost/traindb  \
 --driver org.postgresql.Driver --username train --password Ankara06 \
 --table churn --m 4 --split-by rownumber \
 --hive-import --hive-overwrite  --hive-table test1.churn --target-dir /tmp/churn3
 ```

5. If there is no incremental column in source table like pk sqoop has to use --m 1 means just one mapper


6. Import using where condition
```
sqoop import --connect jdbc:postgresql://localhost/traindb  \
 --driver org.postgresql.Driver --username train --password Ankara06 \
 --query "select * from public.churn where exited = 1  AND \$CONDITIONS" \
 --m 4 --split-by rownumber \
 --hive-import --create-hive-table  --hive-table test1.churn_exited_1 --target-dir /tmp/churn_exited_1
 ```

Check result from DBeaver
` select COUNT(1) from test1.churn_exited_1 where exited = 0; `
Output should be 0

`select COUNT(1) from test1.churn_exited_1 where exited = 1;`
Output should be 2037

7. Run sqoop as a script
```
[train@localhost play]$ cat run_sqoop.sh
#!/bin/bash
 sqoop import --connect jdbc:postgresql://localhost/traindb  --driver org.postgresql.Driver --username train --password Ankara06 --query "select * from churn WHERE \$CONDITIONS" --m 4 --split-by rownumber --hive-import  --create-hive-table --hive-table test2.churn --target-dir /tmp/churn

[train@localhost play]$ ./run_sqoop.sh > sqoop.log 2>1&
 ```
