1. For incremental import sqoop just brings new records to do so it needs a column that always increses when new rows
inserted or updated. An timestamp type is ideal for this purpose when ever a record insert, delete, update this column
will always greter than old  or previous one.

2. Create new table in postgresql (Debeaver)
```
SET timezone = 'Europe/Istanbul';


create table if not exists world_classics (
  id              serial primary key,
  title           varchar(100) not null,
  author  varchar(100) null,
  updation timestamp WITH time ZONE DEFAULT current_timestamp,
  status char(1) not null
);

create sequence world_classics_sequence
  start 150181501
  increment 1;


insert into world_classics
  (id, title, author,status)
values
  (nextval('world_classics_sequence'), 'Hamlet', 'William Shakespeare','I'),
  (nextval('world_classics_sequence'), 'The Great Gatsby', ' F. Scott Fitzgerald','I'),
  (nextval('world_classics_sequence'), 'Jane Eyre', ' Charlotte Brontë','I'),
  (nextval('world_classics_sequence'), 'The Picture of Dorian Gray', 'Oscard Wilde','I'),
  (nextval('world_classics_sequence'), 'The Canterbury Tales', 'Geoffrey Chaucer','I'),
  (nextval('world_classics_sequence'), 'Nineteen Eighty-Four', 'George Orwell','I'),
  (nextval('world_classics_sequence'), 'Crime and Punishment', 'Fyodor Dostoyevsky','I'),
  (nextval('world_classics_sequence'), 'Pride and Prejudice', ' Jane Austen','I'),
  (nextval('world_classics_sequence'), 'Wuthering Heights', 'Emily Brontë','I'),
  (nextval('world_classics_sequence'), 'Aesops Fables ', 'La Fontaine','I');

```
```
select * from world_classics ;
id       |title                     |author              |updation           |status|
---------|--------------------------|--------------------|-------------------|------|
150181501|Hamlet                    |William Shakespeare |2020-09-18 11:19:20|I     |
150181502|The Great Gatsby          | F. Scott Fitzgerald|2020-09-18 11:19:20|I     |
150181503|Jane Eyre                 | Charlotte Brontë   |2020-09-18 11:19:20|I     |
150181504|The Picture of Dorian Gray|Oscard Wilde        |2020-09-18 11:19:20|I     |
150181505|The Canterbury Tales      |Geoffrey Chaucer    |2020-09-18 11:19:20|I     |
150181506|Nineteen Eighty-Four      |George Orwell       |2020-09-18 11:19:20|I     |
150181507|Crime and Punishment      |Fyodor Dostoyevsky  |2020-09-18 11:19:20|I     |
150181508|Pride and Prejudice       | Jane Austen        |2020-09-18 11:19:20|I     |
150181509|Wuthering Heights         |Emily Brontë        |2020-09-18 11:19:20|I     |
150181510|Aesops Fables             |La Fontaine         |2020-09-18 11:19:20|I     |
```



 2. First import
```
sqoop import --connect jdbc:postgresql://localhost/traindb \
--driver org.postgresql.Driver \
--username train --password Ankara06 \
--query "select id, title, author, updation,status from world_classics WHERE \$CONDITIONS" \
--m 1  \
--hive-import  --create-hive-table --hive-table test1.world_classics \
--target-dir /tmp/world_classics
```

3. Check hive
```
select * from test1.world_classics;
id       |title                     |author              |updation                  |status|
---------|--------------------------|--------------------|--------------------------|------|
150181501|Hamlet                    |William Shakespeare |2020-09-18 11:19:20.324344|I     |
150181502|The Great Gatsby          | F. Scott Fitzgerald|2020-09-18 11:19:20.324344|I     |
150181503|Jane Eyre                 | Charlotte Brontë   |2020-09-18 11:19:20.324344|I     |
150181504|The Picture of Dorian Gray|Oscard Wilde        |2020-09-18 11:19:20.324344|I     |
150181505|The Canterbury Tales      |Geoffrey Chaucer    |2020-09-18 11:19:20.324344|I     |
150181506|Nineteen Eighty-Four      |George Orwell       |2020-09-18 11:19:20.324344|I     |
150181507|Crime and Punishment      |Fyodor Dostoyevsky  |2020-09-18 11:19:20.324344|I     |
150181508|Pride and Prejudice       | Jane Austen        |2020-09-18 11:19:20.324344|I     |
150181509|Wuthering Heights         |Emily Brontë        |2020-09-18 11:19:20.324344|I     |
150181510|Aesops Fables             |La Fontaine         |2020-09-18 11:19:20.324344|I     |
```
schema
```
describe test1.world_classics;
col_name|data_type|comment|
--------|---------|-------|
id      |int      |       |
title   |string   |       |
author  |string   |       |
updation|string   |       |
status  |string   |       |
```
updation doesn't seem to fit timestamp but no problem.




4. Add Postgresql new records
```
insert into world_classics
  (id, title, author,status)
values
  (nextval('world_classics_sequence'), 'The Tenant of Wildfell Hall', ' Anne Brontë','I'),
  (nextval('world_classics_sequence'), 'Frankenstein', 'Mary Wollstonecraft Shelley','I'),
  (nextval('world_classics_sequence'), 'Gullivers Travels', 'Jonathan Swift','I'),
  (nextval('world_classics_sequence'), 'Oliver Twist', 'Charles Dickens','I');
```

4. Run sqoop incremental import We expect just newly added records
```
sqoop import --connect jdbc:postgresql://localhost/traindb \
--driver org.postgresql.Driver \
--username train --password Ankara06 \
--query "select id, title, author, updation, status from world_classics WHERE \$CONDITIONS" \
--m 2 --split-by id \
--check-column updation \
--merge-key id \
--incremental lastmodified \
--last-value "2020-09-18 11:20:00" \
--hive-import --hive-table test1.world_classics \
--target-dir /tmp/world_classics_diff
```

this gives an error
```
2020-09-18 18:24:03,176 ERROR tool.ImportTool: Encountered IOException running import job: java.io.IOException: Could not get current time from database
```
It is a bug sqoop wants to learn current_timestamp from postgresql with `current_timestamp()`
but in postgresql it is `current_timestamp`
