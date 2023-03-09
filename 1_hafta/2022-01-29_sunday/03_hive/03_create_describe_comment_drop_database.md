### 1. Create database
` create database if not exists test1; `

Close logs  
`  0: jdbc:hive2://127.0.0.1:10000> set hive.server2.logging.operation.level=NONE;  `   

### 2. List databases
```
show databases;
+----------------+
| database_name  |
+----------------+
| default        |
| test1          |
+----------------+
4 rows selected (0.086 seconds)
```

### 3. Describe database
```
describe database test1;
+----------+----------+----------------------------------------------------+-------------+-------------+-------------+
| db_name  | comment  |                      location                      | owner_name  | owner_type  | parameters  |
+----------+----------+----------------------------------------------------+-------------+-------------+-------------+
| test1    |          | hdfs://localhost:9000/user/hive/warehouse/test1.db | train       | USER        |             |
+----------+----------+----------------------------------------------------+-------------+-------------+-------------+
1 row selected (0.077 seconds)
```

### 4. Drop database
```
drop database test1;
No rows affected (0.302 seconds)


show databases;
+----------------+
| database_name  |
+----------------+
| bookstore      |
| default        |
| train          |
+----------------+
```

- **If we want to delete database including the all tables in it**
` DROP DATABASE database_name CASCADE; `

### 5. We can add comments to databases
```
create database if not exists test1 comment 'This db is for big data training.';
No rows affected (0.085 seconds)
describe database test1;
+----------+------------------------------------+----------------------------------------------------+-------------+-------------+-------------+
| db_name  |              comment               |                      location                      | owner_name  | owner_type  | parameters  |
+----------+------------------------------------+----------------------------------------------------+-------------+-------------+-------------+
| test1    | This db is for big data training.  | hdfs://localhost:9000/user/hive/warehouse/test1.db | train       | USER        |             |
+----------+------------------------------------+----------------------------------------------------+-------------+-------------+-------------+
1 row selected (0.115 seconds)
```

### 6. What happens when we create database?
- db hdfs location 
- Metadata
- File and metadata ownership